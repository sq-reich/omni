import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-home',
  standalone: true,  // ← wichtig!

  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonicModule]
})
export class HomePage implements OnInit {
  frei: number = 0;
  torOffen: boolean = false;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.update();
    setInterval(() => this.update(), 3000);
  }

  update() {
    this.api.getStatus().subscribe((res: any) => {
      this.frei = res.frei;
      this.torOffen = res.tor_offen;
    });
  }

  torAuf() {
    this.api.torAuf().subscribe(() => this.update());
  }

  torZu() {
    this.api.torZu().subscribe(() => this.update());
  }
}
