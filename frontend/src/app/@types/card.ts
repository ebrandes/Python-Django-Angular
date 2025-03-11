import { Brand } from './brand';

export interface Card {
  id: number;
  user: number;
  lastFourDigits: string;
  holder: string;
  expiryYear: string;
  expiryMonth: string;
  brand: Brand;
}
