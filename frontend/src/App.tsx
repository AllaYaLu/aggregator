import { useEffect, useState } from 'react';
import type { BankCard } from './types/card';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export function App() {
  const [cards, setCards] = useState<BankCard[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Фильтры
  const [cardType, setCardType] = useState<string>('');
  const [freeOnly, setFreeOnly] = useState<boolean>(false);
  const [minCashback, setMinCashback] = useState<string>('');

  useEffect(() => {
    const fetchCards = async () => {
      setLoading(true);
      setError(null);

      try {
        const params = new URLSearchParams();
        if (cardType) params.append('card_type', cardType);
        if (freeOnly) params.append('free_only', 'true');
        if (minCashback) params.append('min_cashback', minCashback);

        const response = await fetch(`${API_URL}/api/cards?${params.toString()}`);
        if (!response.ok) {
          throw new Error('Не удалось загрузить предложения банков');
        }

        const data: BankCard[] = await response.json();
        setCards(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Ошибка соединения с сервером');
      } finally {
        setLoading(false);
      }
    };

    fetchCards();
  }, [cardType, freeOnly, minCashback]);

  return (
    <div>
      {/* Фирменная шапка НАЙДУ.ONLINE */}
      <header className="header">
        <div className="header-container">
          <a href="/" className="logoStyle2">
            <span className="logoBase">НАЙ</span>
            <span className="logoGlow">ДУ</span>
            <span className="domainStyle2">.online</span>
          </a>
          <span className="header-subtitle">Умный подбор банковских карт</span>
        </div>
      </header>

      <main className="main-container">
        <h1>Подбор банковских карт</h1>

        {/* Панель фильтров */}
        <section className="filters-panel">
          <div className="filter-group">
            <label className="filter-label">Тип карты</label>
            <select
              className="filter-input"
              value={cardType}
              onChange={(e) => setCardType(e.target.value)}
            >
              <option value="">Все карты</option>
              <option value="debit">Дебетовые</option>
              <option value="credit">Кредитные</option>
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label">Кэшбэк от (%)</label>
            <input
              type="number"
              className="filter-input"
              min="0"
              max="100"
              placeholder="Например, 5"
              value={minCashback}
              onChange={(e) => setMinCashback(e.target.value)}
            />
          </div>

          <label className="checkbox-wrapper">
            <input
              type="checkbox"
              checked={freeOnly}
              onChange={(e) => setFreeOnly(e.target.checked)}
            />
            <span>Только бесплатное обслуживание</span>
          </label>
        </section>

        {/* Состояния */}
        {loading && <div className="status-box">Загружаем актуальные предложения...</div>}

        {error && (
          <div className="status-box" style={{ color: '#c0392b' }}>
            {error}. Убедитесь, что бэкенд запущен.
          </div>
        )}

        {!loading && !error && cards.length === 0 && (
          <div className="status-box">
            <p>По выбранным фильтрам карт не найдено.</p>
            <button
              className="link-detail"
              onClick={() => {
                setCardType('');
                setFreeOnly(false);
                setMinCashback('');
              }}
            >
              Сбросить фильтры
            </button>
          </div>
        )}

        {/* Сетка карточек */}
        <div className="cards-grid">
          {cards.map((card) => (
            <article key={card.id} className="card">
              <div>
                {/* Шапка карточки: логотип + название банка + бейдж типа */}
                <div className="card-header">
                  <div className="bank-info">
                    <div className="bank-logo-container">
                      {card.image_url ? (
                        <img
                          src={card.image_url}
                          alt={card.bank_name}
                          className="bank-logo-img"
                        />
                      ) : (
                        <div className="bank-logo-placeholder">
                          {card.bank_name.charAt(0)}
                        </div>
                      )}
                    </div>
                    <span className="bank-name">{card.bank_name}</span>
                  </div>

                  <span className="card-type-badge">
                    {card.card_type === 'debit' ? 'Дебетовая' : 'Кредитная'}
                  </span>
                </div>

                {/* Название карты */}
                <h2 className="card-title">{card.name}</h2>

                {/* Список условий */}
                <div className="features-list">
                  <div className="feature-item">
                    <span>Кэшбэк до</span>
                    <span className="feature-value">{card.cashback_percent}%</span>
                  </div>
                  <div className="feature-item">
                    <span>Обслуживание</span>
                    <span className="feature-value">
                      {card.annual_fee === 0 ? 'Бесплатно' : `${card.annual_fee} ₽/год`}
                    </span>
                  </div>
                </div>
              </div>

              {/* Кнопка оформления */}
              <div>
                <a
                  href={card.apply_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-cta"
                >
                  Оформить карту
                </a>
              </div>
            </article>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
