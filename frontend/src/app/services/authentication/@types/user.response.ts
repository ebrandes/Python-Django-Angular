export interface UserResponse {
  user_id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'user';
}
