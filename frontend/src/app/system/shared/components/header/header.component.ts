import { Component } from '@angular/core';
import { AuthService } from 'src/app/shared/services/auth.service';
import { Router } from '@angular/router';
import { GlobalConfig } from 'src/app/global';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})


export class HeaderComponent {
  isOpen = false;
  open() {
    this.isOpen = !this.isOpen;
  }
  
  flag1=GlobalConfig.flagMenu1;
  flag2=GlobalConfig.flagMenu2;
  flag3=GlobalConfig.flagMenu3;
  
  constructor(
    private router: Router,
    private auth: AuthService
  ) { }
  id: any;
  drop(param: any) {
    this.id = param;
  }

  closeDrop(param: any)
  {
    if (this.id == param) {
       this.id = "";
     }
  }

  logout()
  {
    GlobalConfig.t="";
    this.router.navigate(['/system', 'about-us']);
  }
    
  }

