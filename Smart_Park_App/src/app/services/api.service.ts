import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private BASE_URL = 'http://192.168.178.50:5000'; // Deine Pi-IP

  constructor(private http: HttpClient) {}

  getStatus() {
    return this.http.get(`${this.BASE_URL}/api/status`);
  }

  torAuf() {
    return this.http.get(`${this.BASE_URL}/tor-auf`);
  }

  torZu() {
    return this.http.get(`${this.BASE_URL}/tor-zu`);
  }
}
