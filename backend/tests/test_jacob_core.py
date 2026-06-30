from jacob_core.core import JacobCore
from jacob_core.models import Intent, PartnerMessage


def test_morning_briefing_intent():
    core = JacobCore()
    response = core.handle(PartnerMessage(partner_name="Jason", content="Bom dia, Jacob."))

    assert response.intent == Intent.MORNING_BRIEFING
    assert "Bom dia, Jason" in response.text
    assert response.specialist_name == "Morning Briefing Specialist"


def test_life_analytics_intent():
    core = JacobCore()
    response = core.handle(
        PartnerMessage(partner_name="Jason", content="Como está minha vida em métricas?")
    )

    assert response.intent == Intent.LIFE_ANALYTICS
    assert "Mapa da Vida" in response.text


def test_emotional_support_intent():
    core = JacobCore()
    response = core.handle(PartnerMessage(partner_name="Jason", content="Estou cansado hoje."))

    assert response.intent == Intent.EMOTIONAL_SUPPORT
    assert "Estou com você" in response.text
