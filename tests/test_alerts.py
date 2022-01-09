import pyhvr
from pyhvr.pyhvr_exceptions import PyhvrError

hvr_client = pyhvr.client(
    username="admin", password="Kiwi1234", uri="http://localhost:4340"
)


def test_create_alerts():
    newa = hvr_client.post_hubs_alerts(
        hub="hvrhub",
        alert="alert1",
        props={
            "Ignore_Warnings": "false",
            "Notification_Type": "EMAIL",
            "Email_Recipients": ["sahananagaraj9@gmail.com"],
            "Email_SMTP_Server": "smtp.gmail.com",
            "Email_SMTP_Starttls": "true",
            "Repeat_Interval": "3600",
            "Add_HVR_Event": "true"
        }
    )

    assert newa is None


def test_execute_alerts():
    exa = hvr_client.post_hubs_alerts_execute(hub="hvrhub", alert="alert1")
    assert exa is not None


def test_get_alerts():
    alerts = hvr_client.get_hubs_alerts(hub="hvrhub")
    assert alerts is not None


def test_alerts_props():
    aprops = hvr_client.get_hubs_alerts_props(hub="hvrhub", alert="alert1")
    assert aprops["Email_SMTP_Server"] == "smtp.gmail.com"
    # assert aprops["Email_Recipients"] == "sahananagaraj9@gmail.com"


def test_al_patch():
    ppl = {"Email_Recipients": ["sahana@gmail.com"]}
    testp = hvr_client.patch_hubs_alerts_props(hub="hvrhub", alert="alert1", **ppl)
    assert testp is None


def test_duplicate_alert():
    try:
        hvr_client.post_hubs_alerts(
            hub="hvrhub",
            alert="alert1",
            props={
                "Ignore_Warnings": "false",
                "Notification_Type": "EMAIL",
                "Email_Recipients": ["sahana.nagaraj@fivetran.com"],
                "Email_SMTP_Server": "smtp.gmail.com",
                "Email_SMTP_Starttls": "true",
                "Repeat_Interval": "3600",
                "Add_HVR_Event": "true"
            }
        )
    except PyhvrError as e:
        assert e.error_code == "F_JR2D03"


def test_a_props():
    ppl = {
        "Add_HVR_Event": "true",
        "Email_Recipients": ["sahana.nagaraj@fivetran.com"],
        "Email_SMTP_Server": "smtp.gmail.com",
        "Ignore_Warnings": "false",
        "Notification_Type": "EMAIL",
        "Repeat_Interval": 300,
        "Last_Ran": "2021-12-06T09:13:36Z"
    }

    testp = hvr_client.put_hubs_alerts_props(hub="hvrhub", alert="alert1", **ppl)
    assert testp is None


def test_delete_alert():
    dalert = hvr_client.delete_hubs_alerts(hub="hvrhub", alert="alert1")
    assert dalert is None
