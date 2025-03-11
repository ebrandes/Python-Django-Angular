import { Address } from './address';
import { Card } from './card';
import { Product } from './product';

export interface Cart {
  user: number;
  totalPrice: number;
  items?: Product[];
  address?: Address;
  paymentCard?: Card;
}
