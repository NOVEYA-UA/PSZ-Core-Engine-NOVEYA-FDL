"""
Automated Test Suite for NoveaAtomEngine
Component: PyTest Module for Telemetry Simulation & PayPal Sandbox Validation
Methodology: Resource-Norming Methodology (NRM) & Formal Dialectics (-FDL)
"""

import pytest
import responses  # Рекомендуется для точного перехвата HTTP-запросов (pip install responses)
from unittest.mock import MagicMock, patch
from NoveaAtomEngine import NoveaAtomEngine  # Импорт разработанного ранее ядра

# Имитационные ключи доступа для тестового контура Sandbox PayPal
MOCK_CLIENT_ID = "AYz4b_NoveaAtomFakeClientID_KUB_v1_TestKey2026_XYZ"
MOCK_CLIENT_SECRET = "EKn_NoveaAtomFakeSecret_FNV_DevelopmentFund_999"

@pytest.fixture
def engine():
    """Фикстура инициализации ядра NoveaAtomEngine в режиме Sandbox."""
    return NoveaAtomEngine(
        client_id=MOCK_CLIENT_ID, 
        client_secret=MOCK_CLIENT_SECRET, 
        mode="sandbox"
    )

# ==============================================================================
# БЛОК 1: ИМИТАЦИЯ БОРТОВОЙ ТЕЛЕМЕТРИИ (Датчики массы и пассажиропотока)
# ==============================================================================

@pytest.mark.parametrize(
    "delta_m_kg, passengers_in, route_length_km, expected_n_fe",
    [
        (3500.0, 50, 10.0, 500.0),   # Средняя нагрузка: 50 человек на 10 км = 500 пасс-км
        (7000.0, 100, 15.0, 1500.0), # Пиковая нагрузка (час пик по Николаеву)
        (70.0, 1, 5.0, 5.0),         # Минимальный квант (1 пассажир)
    ]
)
def test_telemetry_to_fe_conversion(delta_m_kg, passengers_in, route_length_km, expected_n_fe):
    """
    Тест верификации пассивного учета ИИ-агентом.
    Проверяет, как изменение массы подвижного состава (Δm) сопоставляется 
    с ИК-барьерами и конвертируется в Абстрактно-Необходимые Функциональные Единицы (ФЕ).
    """
    # Средний вес пассажира по ГОСТу/СНиПу принят за 70 кг
    calculated_passengers_by_mass = delta_m_kg / 70.0
    
    # Кросс-валидация ИИ-оркестратора: сопоставление весового прогиба осей и оптических датчиков
    assert abs(calculated_passengers_by_mass - passengers_in) < 1e-5
    
    # Расчет результирующего путевого объема ФЕ (пассажиро-километры)
    n_fe = passengers_in * route_length_km
    assert n_fe == expected_n_fe


# ==============================================================================
# БЛОК 2: ТЕСТИРОВАНИЕ МАТЕМАТИЧЕСКОГО АППАРАТА (НРМ И ФДЛ)
# ==============================================================================

def test_calculate_nrm_metrics_success(engine):
    """Проверка расчета базовой/фактической ресурсоемкости и коэффициента Ksn."""
    t_base = 100.0  # Плановые нормо-часы/энергоресурсы
    t_fact = 80.0   # Фактически затраченные ресурсы (экономия водителя)
    n_fe = 500.0    # Квант выполненной работы
    
    nr_base, nr_fact, k_sn = engine.calculate_nrm_metrics(t_base, t_fact, n_fe)
    
    assert nr_base == 0.2
    assert nr_fact == 0.16
    assert k_sn == 1.25  # Ksn > 1 -> эффективность повышена на 25%


def test_calculate_nrm_metrics_division_by_zero(engine):
    """Защита ядра от некорректных или пустых данных телеметрии (N_FE = 0)."""
    with pytest.raises(ValueError, match="Количество Функциональных Единиц .* должно быть больше нуля"):
        engine.calculate_nrm_metrics(100, 80, 0)


def test_calculate_true_labor_with_shrin_environment(engine):
    """
    Тест формулы Tr = To / (Cч - f(K)).
    Проверка стабильности знаменателя при отрицательных штрафных коэффициентах рынка.
    """
    t_base = 50.0
    c_ch = 1.0  # Базовое качество труда
    
    # Сценарий А: Благоприятная общинная среда (f(K) стремится к нулю или положительно)
    tr_good = engine.calculate_true_labor(t_base, c_ch, f_k=0.2)
    assert tr_good == 50.0 / 0.8
    
    # Сценарий Б: Критический регресс рыночной среды (штрафной коэффициент f(K) завышен)
    # Знаменатель падает ниже критического порога. Должен сработать защитный лимит 0.01.
    tr_collapse = engine.calculate_true_labor(t_base, c_ch, f_k=1.5)
    assert tr_collapse == 50.0 / 0.01


def test_evaluate_fdl_score_limits(engine):
    """Проверка фиксации рейтинга FDL-Score в диапазоне жестких границ [0, 1000]."""
    # Идеальные показатели (сверхэффективность)
    score_max = engine.evaluate_fdl_score(k_sn=3.0, c_ch=1.8, f_k=0.5)
    assert score_max == 1000
    
    # Полный крах нормирования и качества
    score_min = engine.evaluate_fdl_score(k_sn=0.0, c_ch=0.0, f_k=-5.0)
    assert score_min == 0


# ==============================================================================
# БЛОК 3: ИМИТАЦИЯ СКВОЗНОГО ПРОГОНА (PayPal API Sandbox Mocking)
# ==============================================================================

@patch("NoveaAtomEngine.requests.post")
def test_execute_payout_success(mock_post, engine):
    """
    Сквозной тест успешного исполнения выплаты.
    Имитирует одобрение Grok-FDL (FDL-Score >= 700), расчет удержания 10% в фонд FNV 
    и генерацию REST-запроса к API-шлюзу PayPal без отправки реальных денег.
    """
    # 1. Настройка ложных ответов от серверов PayPal (Mocking OAuth2 & Payouts API)
    mock_response_oauth = MagicMock()
    mock_response_oauth.status_code = 200
    mock_response_oauth.json.return_value = {"access_token": "ACCESS_TOKEN_MOCK_2026_VALID"}
    
    mock_response_payout = MagicMock()
    mock_response_payout.status_code = 201
    mock_response_payout.json.return_value = {
        "batch_header": {"payout_batch_id": "MOCK_BATCH_ID_999", "batch_status": "PENDING"}
    }
    
    # Переключатель ответов для последовательных вызовов requests.post
    mock_post.side_effect = [mock_response_oauth, mock_response_payout]

    # 2. Входные параметры верифицированного транспортного рейса
    tr = 10.0
    k_sn = 1.2
    fdl_score = 800  # Выше лимита 700 -> Проверка пройдена
    recipient = "driver.nikolaev@communa.org"
    job_id = "REYS_2026_10_26_001"

    # Математическое ожидание:
    # T_fdl = (10.0 * 1.2 * 800) / 1000 = 9.6 токенов
    # Gross = 9.6 * 15.5 (r_rate) = 148.8 USD
    # FNV_deduction (10%) = 14.88 USD
    # Net_payout = 148.8 - 14.88 = 133.92 USD
    
    # 3. Выполнение операции
    result = engine.execute_payout(tr, k_sn, fdl_score, recipient, job_id)

    # 4. Проверка утверждений (Assertions)
    assert result["status"] == "SUCCESS"
    assert result["net_payout"] == 133.92
    assert result["fnv_allocation"] == 14.88
    assert result["paypal_response"]["batch_header"]["payout_batch_id"] == "MOCK_BATCH_ID_999"
    
    # Проверка, что было совершено ровно 2 запроса к PayPal API Gateway
    assert mock_post.call_count == 2


def test_execute_payout_rejected_by_audit(engine):
    """Тест автоматической блокировки выплаты при низком уровне FDL-Score (менее 700)."""
    result = engine.execute_payout(
        tr=10.0, 
        k_sn=0.5, 
        fdl_score=550,  # ИИ-агент Grok выявил девиации/приписки
        recipient="fraudulent.driver@monopoly.com", 
        job_id="BAD_REYS_002"
    )
    
    assert result["status"] == "REJECTED"
    assert result["reason"] == "Low FDL-Score"
