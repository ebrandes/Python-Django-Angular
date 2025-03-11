import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../../environments/environment';

export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  req = req.clone({
    url: `${environment.apiBaseUrl}${req.url}`,
    withCredentials: true,
  });
  return next(req);
};
