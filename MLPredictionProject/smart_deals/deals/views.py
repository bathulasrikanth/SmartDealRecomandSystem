# deals/views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .utils import get_model, get_metadata

def home(request):
    return render(request, "home.html")

def predict_coupon(request):
    if request.method != "POST":
        return render(request, "home.html")

    # 1) Collect form values (only fields your form provides)
    form_data = {
        # adapt these keys to your form input names
        "trip_purpose": request.POST.get("trip_purpose", "").strip(),
        "travel_company": request.POST.get("travel_company", "").strip(),
        "current_weather": request.POST.get("current_weather", "").strip(),
        "ambient_temp": request.POST.get("ambient_temp") or None,
        "time_of_day": request.POST.get("time_of_day", "").strip(),
        "offer_type": request.POST.get("offer_type", "").strip(),
        "deal_expiry_window": request.POST.get("deal_expiry_window", "").strip(),
        "user_gender": request.POST.get("user_gender", "").strip(),
        "user_age_group": request.POST.get("user_age_group", "").strip(),
        "relationship_status": request.POST.get("relationship_status", "").strip(),
        # numeric safely cast
        "num_dependents": int(request.POST.get("num_dependents") or 0),
        # if you have previous_redemption etc add here
        "previous_redemption": int(request.POST.get("previous_redemption") or 0),
    }

    # 2) Load model and metadata
    try:
        model = get_model()
    except Exception as e:
        return render(request, "result.html", {
            "message": f"Model load failed: {e}",
            "probability": None,
            "prediction": None,
            "data": form_data
        })

    metadata = get_metadata()  # expected dict like {'numeric_columns': [...], 'categorical_columns': [...], 'target_column': 'redeemed'}

    # 3) Build full input using metadata; if metadata missing, fall back to model's preprocessors
    if metadata:
        numeric_cols = metadata.get("numeric_columns", [])
        categorical_cols = metadata.get("categorical_columns", [])
        full_feature_list = numeric_cols + categorical_cols
    else:
        # fallback: try to infer from pipeline (best-effort)
        # If pipeline available and has preprocessor, attempt to introspect names:
        full_feature_list = []
        try:
            pre = model.named_steps.get("preprocessor", None)
            if pre is not None and hasattr(pre, "transformers_"):
                # This is a best-effort fallback; still safer to have metadata file
                # We'll build a list from transformers_
                num_names = []
                cat_names = []
                for name, trans, cols in pre.transformers_:
                    if name == "num":
                        num_names.extend(cols)
                    if name == "cat":
                        cat_names.extend(cols)
                full_feature_list = num_names + cat_names
        except Exception:
            full_feature_list = []

    # 4) Create full input dict with defaults
    full_input = {}
    for col in full_feature_list:
        if col in form_data and form_data[col] is not None and form_data[col] != "":
            full_input[col] = form_data[col]
            continue

        # Provide sensible defaults based on column name patterns
        if col in form_data:
            full_input[col] = form_data[col]  # may be numeric or string
        elif col in ["ambient_temp", "temperature", "temp"]:
            full_input[col] = float(form_data.get("ambient_temp") or 0.0)
        elif col in ["num_dependents", "previous_redemption"]:
            full_input[col] = int(form_data.get(col) or 0)
        elif col.startswith("visit_") or col.startswith("min_gap_") or col.endswith("_freq") or "visit" in col or "min_gap" in col:
            # frequency/gap fields — default to 0
            try:
                full_input[col] = 0
            except:
                full_input[col] = 0
        else:
            # default categorical filler
            full_input[col] = "Unknown"

    # 5) If there are any additional fields your pipeline expects (direction_match/direction_mismatch)
    # they are likely binary ints (0/1) — ensure numeric 0
    for f in ["direction_match", "direction_mismatch"]:
        if f in full_feature_list and full_input.get(f) in [None, "", "Unknown"]:
            full_input[f] = 0

    # 6) Create DataFrame in proper column order expected by pipeline
    input_df = pd.DataFrame([full_input], columns=full_feature_list)

    # 7) Convert dtypes for numeric columns
    for c in (metadata.get("numeric_columns") if metadata else []):
        if c in input_df.columns:
            input_df[c] = pd.to_numeric(input_df[c], errors="coerce").fillna(0)

    # 8) Make prediction
    try:
        proba = model.predict_proba(input_df)[:, 1][0]
        pred = int(model.predict(input_df)[0])
    except Exception as e:
        return render(request, "result.html", {
            "message": f"Prediction failed: {e}",
            "probability": None,
            "prediction": None,
            "data": full_input
        })

    message = "Eligible — User Will Likely Redeem The Coupon 🎉" if pred == 1 else "Not Eligible — User Unlikely to Redeem ❌"

    return render(request, "result.html", {
        "probability": round(float(proba), 3),
        "prediction": pred,
        "message": message,
        "data": full_input
    })
