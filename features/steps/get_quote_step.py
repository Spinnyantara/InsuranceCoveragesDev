from behave import given, when, then
import json
from src.utils.request_builder import RequestBuilder
import smtplib
from email.message import EmailMessage
import os
import logging

# Fixed log file path
LOG_FILE_PATH = "logs/latest_quotes_run.log"

# Create log directory if not present
os.makedirs("logs", exist_ok=True)


# Log helper
def log_to_file(text):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(text + "\n")


@given("I load multiple lead payloads from file")
def step_impl(context):
    import json
    with open("data/leads.json", "r") as f:
        context.payloads = json.load(f)


@when("I create lead for each reg no")
def step_impl(context):
    context.leads_info = []

    for payload in context.payloads:
        reg_no = payload["car_registration_number"]
        print(f"\n📤 Sending for reg_no: {reg_no}")

        response = RequestBuilder.post(
            url="https://api-dev.spinnyinsurance.com/sp-insurance-platform/api/v1/leads/get-or-create-lead/",
            data=payload,
            token=context.token
        )

        assert response.status_code == 200, f"❌ API failed for {reg_no}"
        data = response.json()
        lead_id = data["lead_id"]

        car_info = data.get("car_info", {})  # This assumes your response contains product info
        if not car_info:
            print(f"⚠️ Missing car_info for lead: {lead_id}, reg_no: {reg_no}")
            continue

        # Extract individual sections
        vehicle_details = car_info.get("vehicleDetails", {}),
        previous_policy_details = car_info.get("previousPolicyDetails", {})
        customer_details = car_info.get("customerDetails", {})
        new_insurance_details = car_info.get("newInsuranceDetails", {})
        nominee_details = car_info.get("nomineeDetails", {})

        # Assemble the full product details
        product_details = {
            "regNo": car_info.get("regNo", reg_no),
            "chassis": car_info.get("chassis"),
            "engine": car_info.get("engine"),
            "vehicleClass": car_info.get("vehicleClass"),
            "vehicleManufacturerName": car_info.get("vehicleManufacturerName"),
            "model": car_info.get("model"),
            "enMake": car_info.get("enMake"),
            "enModel": car_info.get("enModel"),
            "variant": car_info.get("variant"),
            "vehicleColour": car_info.get("vehicleColour"),
            "type": car_info.get("type"),
            "owner": car_info.get("owner"),
            "regAuthority": car_info.get("regAuthority"),
            "rtoCode": car_info.get("rtoCode"),
            "regDate": car_info.get("regDate"),
            "vehicleManufacturingMonthYear": car_info.get("vehicleManufacturingMonthYear"),
            "rcExpiryDate": car_info.get("rcExpiryDate"),
            "vehicleTaxUpto": car_info.get("vehicleTaxUpto"),
            "vehicleInsuranceCompanyName": car_info.get("vehicleInsuranceCompanyName"),
            "vehicleInsuranceUpto": car_info.get("vehicleInsuranceUpto"),
            "rcFinancer": car_info.get("rcFinancer"),
            "presentAddress": car_info.get("presentAddress"),
            "permanentAddress": car_info.get("permanentAddress"),
            "vehicleCubicCapacity": car_info.get("vehicleCubicCapacity"),
            "grossVehicleWeight": car_info.get("grossVehicleWeight"),
            "vehicleSeatCapacity": car_info.get("vehicleSeatCapacity"),
            "vehicleNumber": car_info.get("vehicleNumber"),
            "puccNumber": car_info.get("puccNumber"),
            "puccUpto": car_info.get("puccUpto"),
            "blacklistStatus": car_info.get("blacklistStatus"),
            "financed": car_info.get("financed"),
            "vehicleExShowroomPrice": car_info.get("vehicleExShowroomPrice"),
            "vcd": car_info.get("vcd"),
            "src": car_info.get("src"),
            "lrt": car_info.get("lrt"),
            "vehicleDetails": {
                "make": vehicle_details[0].get("make"),
                "model": vehicle_details[0].get("model"),
                "modelImage": vehicle_details[0].get("modelImage"),
                "enMMVId": vehicle_details[0].get("enMMVId"),
                "variant": vehicle_details[0].get("variant"),
                "rtoCode": {
                    "internalName": vehicle_details[0].get("rtoCode", {}).get("internalName"),
                    "displayName": vehicle_details[0].get("rtoCode", {}).get("displayName")
                },
                "dateOfRegistration": vehicle_details[0].get("dateOfRegistration"),
                "usedVehicle": vehicle_details[0].get("usedVehicle"),
                "registrationNo": vehicle_details[0].get("registrationNo"),
                "engineNo": vehicle_details[0].get("engineNo"),
                "chassisNo": vehicle_details[0].get("chassisNo"),
                "manufactureDate": vehicle_details[0].get("manufactureDate"),
                "isVehicleFinanced": vehicle_details[0].get("isVehicleFinanced"),
                "financierName": vehicle_details[0].get("financierName"),
                "financierAddress": vehicle_details[0].get("financierAddress"),
                "newVehicle": vehicle_details[0].get("newVehicle"),
                "vehicleType": vehicle_details[0].get("vehicleType")
            },
            "previousPolicyDetails": {
                "applicablePlanTypes": previous_policy_details.get("applicablePlanTypes", []),
                "insurerCode": previous_policy_details.get("insurerCode"),
                "validTill": previous_policy_details.get("validTill"),
                "hasFiledClaim": previous_policy_details.get("hasFiledClaim"),
                "tpExpiryDate": previous_policy_details.get("tpExpiryDate"),
                "odExpiryDate": previous_policy_details.get("odExpiryDate"),
                "policyNumber": previous_policy_details.get("policyNumber"),
                "isVehicleHypothicated": previous_policy_details.get("isVehicleHypothicated"),
                "tpStartDate": previous_policy_details.get("tpStartDate"),
                "currentTPInsurerCode": previous_policy_details.get("currentTPInsurerCode"),
                "currentTPPolicyNumber": previous_policy_details.get("currentTPPolicyNumber"),
                "applicableNoClaimBonus": previous_policy_details.get("applicableNoClaimBonus", []),
                "recommendedPlanType": previous_policy_details.get("recommendedPlanType", {}),
                "suggestedNoClaimBonus": previous_policy_details.get("suggestedNoClaimBonus", {}),
                "manualNoClaimBonus": previous_policy_details.get("manualNoClaimBonus", {}),
                "manualPreviousPlanType": previous_policy_details.get("manualPreviousPlanType", {})
            },
            "customerDetails": {
                "title": customer_details.get("title"),
                "fullName": customer_details.get("fullName"),
                "mobileNumber": customer_details.get("mobileNumber"),
                "pincode": customer_details.get("pincode"),
                "emailId": customer_details.get("emailId"),
                "address1": customer_details.get("address1"),
                "address2": customer_details.get("address2"),
                "customerType": customer_details.get("customerType"),
                "gender": customer_details.get("gender"),
                "dobOrDoi": customer_details.get("dobOrDoi"),
                "city": customer_details.get("city"),
                "state": customer_details.get("state")
            },
            "newInsuranceDetails": {
                "applicablePlanTypes": new_insurance_details.get("applicablePlanTypes", []),
                "recommendedPlanType": new_insurance_details.get("recommendedPlanType", {})
            },
            "nomineeDetails": {
                "nomineeName": nominee_details.get("nomineeName"),
                "nomineeDOB": nominee_details.get("nomineeDOB"),
                "relationshipWithNominee": nominee_details.get("relationshipWithNominee"),
                "nomineeGender": nominee_details.get("nomineeGender"),
                "appointeeName": nominee_details.get("appointeeName"),
                "nomineeRelationshipWithAppointee": nominee_details.get("nomineeRelationshipWithAppointee")
            }
        }

        context.leads_info.append({
            "lead_id": lead_id,
            "product_details": product_details,
            "reg_no": reg_no
        })
        print(f"✅ reg_no: {reg_no} → lead_id: {lead_id}")


@when("I update product details for each lead")
def step_impl(context):
    context.updated_leads = []

    for lead in context.leads_info:
        update_payload = {
            "lead_id": lead["lead_id"],
            "product_details": lead["product_details"]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {context.token}",
            "Cookie": f"access_token={context.token}"
        }

        # print(f"📤 Updating product... details for lead_id: {lead['lead_id']}")

        update_response = RequestBuilder.post(
            url="https://api-dev.spinnyinsurance.com/sp-insurance-platform/api/v1/leads/update-product-details/",
            data=update_payload,
            token=context.token,
            headers=headers
        )

        if update_response.status_code != 200:
            print(f"🔴 Status Code: {update_response.status_code}")
            print(f"🔴 Response Body: {update_response.text}")

        assert update_response.status_code == 200, f"❌ Update failed for lead_id: {lead['lead_id']}, reg_no: {lead['reg_no']}"
        print(f"✅ Updated lead: {lead['lead_id']}")
        # print(f"Updated Payload for lead {lead['lead_id']}:")
        # print(json.dumps(update_payload, indent=2))
        context.updated_leads.append(lead)


@when("I fetch quotes for each updated lead")
def step_impl(context):
    context.quotes_responses = []
    context.failed_quotes = []

    # Clear previous log content and start fresh
    with open("logs/latest_quotes_run.log", "w", encoding="utf-8") as f:
        f.write("=== New Quotes Run ===\n")

    for lead in context.updated_leads:
        payload = {
            "plan_type": "all",
            "lead_id": lead["lead_id"],
            "no_claim_bonus": 50,
            "idv": "minimumIdv",
            "coverages": {}
        }

        try:
            # log_to_file(f"📤 Fetching quotes for lead_id: {lead['lead_id']}")

            response = RequestBuilder.post(
                url="https://api-dev.spinnyinsurance.com/sp-insurance-platform/api/v1/leads/get-quotes/",
                data=payload,
                token=context.token
            )

            if response.status_code != 200:
                log_to_file(f"❌ Failed for lead {lead['lead_id']}")
                log_to_file(f"🔴 Status Code: {response.status_code}")
                log_to_file(f"🔴 Response Body: {response.text}")

                context.failed_quotes.append({
                    "lead_id": lead["lead_id"],
                    "reg_no": lead["reg_no"],
                    "status_code": response.status_code,
                    "error": response.text
                })
                continue

            assert response.status_code == 200, f"❌ Get Quote Failed for lead {lead['lead_id']}"
            log_to_file(f"✅ Fetched quotes for : {lead['lead_id']} and {lead["reg_no"]}")
            data = response.json()
            context.quotes_responses.append(data)
            log_to_file(json.dumps(data, indent=2))

        except Exception as e:
            log_to_file(f"❌ Exception while fetching quotes for lead {lead['lead_id']}: {str(e)}")
            context.failed_quotes.append({
                "lead_id": lead["lead_id"],
                "error": str(e)
            })
            continue

    log_to_file("\n🔚 Finished fetching quotes.")
    if context.failed_quotes:
        log_to_file(f"\n❗ Some leads failed to fetch quotes:")
        for failure in context.failed_quotes:
            log_to_file(
                f"Lead ID: {failure['lead_id']}, Error: {failure.get('error', 'N/A')}, Status Code: {failure.get('status_code', 'N/A')}")


@then("each quote response should contain valid insurer data")
def step_impl(context):
    all_passed = True
    failed_quotes_summary = []
    success_quotes_summary = []

    for i, quote_response in enumerate(context.quotes_responses):
        try:
            assert quote_response["success"] is True, f"❌ Quotes fetch failed for response {i + 1}"
            assert "quotes" in quote_response and len(
                quote_response["quotes"]) > 0, f"❌ No quotes found in response {i + 1}"

            quote_lines = []
            for quote in quote_response["quotes"]:
                insurer_code = quote["data"]["insurerCode"]
                quote_plan_id = quote["quote_plan_id"]
                quote_id = quote["quote_id"]
                plan_type = quote["plan_type"]
                ncb = quote.get("no_claim_bonus")

                line = (
                    f"✅ Quote {i + 1}: InsurerCode= {insurer_code} "
                    f"PlanType= {plan_type} "
                    f"QuoteId= {quote_id} "
                    f"QuotePlanId= {quote_plan_id} "
                    f"NCB= {ncb}"
                )
                print(line)
                quote_lines.append(line)

        except AssertionError as e:
            all_passed = False
            message = f"❌ Error in quote response {i + 1}: {str(e)}\nResponse Data: {quote_response}"
            print(message)
            logging.error(message)
            failed_quotes_summary.append(f"Response {i + 1}: {str(e)}")

    if all_passed:
        # Send success email
        summary = "\n\n".join(success_quotes_summary)
        subject = "✅ All Quote Validations Passed"
        body = f"All quote responses passed validation.\n\n{summary}"
        send_success_email(subject, body, ["qa-team@example.com"])
    else:
        print("\n🔴 Summary of Failed Quote Validations:")
        for item in failed_quotes_summary:
            print(f"- {item}")
        logging.error("Summary of Failures:\n" + "\n".join(failed_quotes_summary))
        assert False


def send_success_email(subject, body, to_emails):
    msg = EmailMessage()
    msg["Subject"] = "Quote Fetch Automation Log Report"
    msg["From"] = "antara.patil@spinny.com"
    msg["To"] = "daanish.kaul@spinny.com"
    msg.set_content("Please find the attached quote fetch log report.")

    # Attach the log file
    with open(LOG_FILE_PATH, "rb") as f:
        msg.add_attachment(f.read(), filename="latest_quotes_run.log", maintype="text", subtype="plain")

    # Send the email (example uses Gmail)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("antara.patil@spinny.com", "cgkxofhcmltuviww")
            smtp.send_message(msg)
            print("📧 Email has been sent successfully to recipient@example.com ✅")
    except Exception as e:
        print("❌ Failed to send email:", str(e))

