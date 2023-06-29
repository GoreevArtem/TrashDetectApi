import { Component, OnInit } from '@angular/core';
import { AuthService,JWT_NAME } from 'src/app/shared/services/auth.service';
import { Router } from '@angular/router';
import { GlobalConfig } from 'src/app/global';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})


export class HeaderComponent implements OnInit{
  isOpen = false;
  id: any;
  flag1 = true;
  flag2 = false;
  flag3 = false;
  open() {
    this.isOpen = !this.isOpen;
  }

  constructor(
    private router: Router,
    private auth: AuthService
  ) { }
  ngOnInit(): void {
    this.flag1 = !this.auth.isAuthenticated();
    this.flag2 = this.auth.isAuthenticated();
    this.flag3 = this.auth.isAuthenticated();
    }


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
  localStorage.removeItem(JWT_NAME);
  this.router.navigate(['/system', 'about-us']);
  location.reload();
  }
    
  }

