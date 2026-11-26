export interface BankCard {
    id: number;
    name: string;
    bank_name: string;
    card_type: 'debit' | 'credit';
    annual_fee: number;
    cashback_percent: number;
    apply_url: string;
    image_url?: string | null; // Используем как логотип банка (если пусто — сработает круглая заглушка с первой буквой!)
  }
  