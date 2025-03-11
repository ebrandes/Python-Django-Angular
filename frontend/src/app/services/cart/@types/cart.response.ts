import { Brand } from '../../../@types/brand';

export interface CartResponse {
  user: number;
  total_price: number;
  items: CartProductResponse[];
  address?: CartAddressResponse;
  payment_card?: CartCardResponse;
}

export interface CartProductResponse {
  id: number;
  product_name: string;
  product_description: string;
  quantity: number;
  product_price: number;
  product_is_available: boolean;
  total_price: number;
}

export interface CartAddressResponse {
  id: number;
  user: number;
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
  active: boolean;
  selected: boolean;
}

export interface CartCardResponse {
  id: number;
  user: number;
  last_four_digits: string;
  holder: string;
  expiry_year: string;
  expiry_month: string;
  brand: Brand;
}
