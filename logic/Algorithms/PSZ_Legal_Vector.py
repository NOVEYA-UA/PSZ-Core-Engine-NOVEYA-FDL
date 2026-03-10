import math

class LegalVector:
    """Алгоритм перевода жалоб в юридические векторы"""
    
    def __init__(self, raw_data):
        self.to = raw_data.get('to', 0)    # Общественная значимость
        self.sch = raw_data.get('sch', 1.0) # Канон СВЕТ
        self.k = raw_data.get('k', 0)      # Опір
        
    def calculate_resonance(self):
        f_k = self.k * 0.5
        tr = (self.to * self.sch) - f_k
        return round(tr, 1)

    def get_fdl_status(self, tr):
        if tr >= 5:
            return "АКТИВНЫЙ ВЕКТОР (Требуется вмешательство ПСЗ)"
        return "ФОНОВЫЙ ПРОЦЕСС"

# Биомеханическая синхронизация: 'Crane wedge' (Журавлиный клин)
def group_sync(agents):
    return "Синхронизация по ведущему вектору активирована"
