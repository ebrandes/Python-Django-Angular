export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  isAvailable: boolean;
  totalPrice?: number;
  quantity?: number;
}
