import { Component, OnInit } from '@angular/core';
import { ExpertService } from 'src/app/shared/services/expert.service';
import { GlobalConfig } from 'src/app/global';
import { Router } from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { matchpassword } from 'src/app/auth/matchpassword.validator';
import { Card } from 'src/app/shared/model/card.model';
import { RequestsExService } from 'src/app/shared/services/requestsEx.service';
import { PhotoService } from 'src/app/shared/services/photo.service';
import { JWT_NAME } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-requests',
  templateUrl: './requests.component.html',
  styleUrls: ['./requests.component.css']
})

export class RequestsComponent implements OnInit
{
  email: string = "";
  mainCont=true;
  form1: FormGroup=new FormGroup({});
  trueMessageP='The old password has been entered';
  resMessage='';
  isOpen1 = false;
  mas = [{}];
  res: { [index: number]: any; } = {};
  count = 0;
  value: { [index: string]: any; } = {};
  arr: Card[] = [];
  arrOptionReq: Card[] = [];
  j = 0;
  flag=true;
  formPass=false;

  constructor(private expertService:ExpertService, private router:Router,
     private reqEx:RequestsExService, private photoService:PhotoService) { }
  ngOnInit(): void {
    this.expertService.getExpert()
    .subscribe((response:any)=>{
      this.email=response["login"];
    });
    this.form1 = new FormGroup({
      password: new FormControl(null, [Validators.required, Validators.minLength(6)]),
      confirmPassword: new FormControl(null)
    },
    {
      validators:matchpassword
    });

    this.reqEx.getRequests(10)
    .subscribe(result => {
      this.mas.push(result);
      this.res = this.mas[1];
      for (let key in this.res) {
        this.count += 1;
      }
      for (let key in this.res) {
        this.value = this.res[key];
        let card: Card = new Card();
        for (let k in this.value) {
          if (k == 'id') {
            card.id = this.value[k];
          }

          let strTmp = '';
          if (k == 'address') {
            let dict = this.value[k];
            for (let i in dict) {
              if (i == 'address_city') {
                strTmp += dict[i] + ', ';
              }
              if (i == 'address_street') {
                strTmp += dict[i] + ', ';
              }
              if (i == 'address_house_number') {
                strTmp += dict[i];
              }
            }
            card.adress = strTmp;
          }
          if (k == 'garbage_classes' && this.value[k] != null) {
            card.class_trash=this.value[k];
          }
         
          if (k == 'request_date') {
            let tmp: string = this.value[k];
            let st = "";
            for (let i = 0; i < tmp.length; i++) {
              if (tmp[i] != 'T') {
                st += tmp[i];
              }
              else {
                break;
              }
            }
            card.request_date = st;
          }

          if (k == 'status') {
            card.status=this.value[k];
          }
        }
        this.arr[this.j++] = card;
      }
    }
    );
    
  }

  searchText = '';

  openCard(id:any){
    var obj= {
      idReq:id,
      type:'number'
    } 
    localStorage.setItem('idReq',JSON.stringify(obj));
    this.router.navigate(['/expert','request']);
  }

  logout()
  {
    localStorage.removeItem(JWT_NAME);
    this.router.navigate(['/system', 'about-us']);
    location.reload();
  }

  get password(): FormControl {
    return this.form1.get('password') as FormControl;
  }

  changePassword()
  {
    const passwd=this.password.value;
    this.expertService.updatePassword({
      "password":passwd
    })
    .subscribe({
      next:(res)=>{
        this.form1.reset();
        GlobalConfig.t="";
        this.router.navigate(['login']);
      },
      error:(err)=>{
        this.resMessage=err["error"]["detail"];
       if(this.resMessage==this.trueMessageP)
       {
        this.isOpen1=true;
        this.resMessage='';
       }
      }
    })
  }

  change()
  {
    this.formPass=true;
  }

  close1()
  {
    this.isOpen1=false;
    this.form1.reset();
  }

  newReq()
  {
    this.j=0;
    this.arrOptionReq=[];
    this.mainCont=false;
    for (let key in this.res) {
      this.value = this.res[key];
      let card: Card = new Card();
      for (let k in this.value) {
        if (k == 'id') {
          card.id = this.value[k];
        }

        let strTmp = '';
        if (k == 'address') {
          let dict = this.value[k];
          for (let i in dict) {
            if (i == 'address_city') {
              strTmp += dict[i] + ', ';
            }
            if (i == 'address_street') {
              strTmp += dict[i] + ', ';
            }
            if (i == 'address_house_number') {
              strTmp += dict[i];
            }
          }
          card.adress = strTmp;
        }
        
        if (k == 'garbage_classes' && this.value[k] != null) {
          card.class_trash=this.value[k];
        }
        if (k == 'request_date') {
          let tmp: string = this.value[k];
          let st = "";
          for (let i = 0; i < tmp.length; i++) {
            if (tmp[i] != 'T') {
              st += tmp[i];
            }
            else {
              break;
            }
          }
          card.request_date = st;
        }

        if (k == 'status') {
          if (this.value[k] == 'not view') {
            card.status=this.value[k];
          }
          else{
            this.flag=false;
            break;
          }
        }
      }
      if(this.flag==true)
        {
          this.arrOptionReq[this.j++] = card;
        }
        else{
          this.flag=true;
        }
    }
    this.flag=true;
  }

  viewedReq()
  {
    this.j=0;
    this.arrOptionReq=[];
    this.mainCont=false;
    for (let key in this.res) {
      this.value = this.res[key];
      let card: Card = new Card();
      for (let k in this.value) {
        if (k == 'id') {
          card.id = this.value[k];
        }

        let strTmp = '';
        if (k == 'address') {
          let dict = this.value[k];
          for (let i in dict) {
            if (i == 'address_city') {
              strTmp += dict[i] + ', ';
            }
            if (i == 'address_street') {
              strTmp += dict[i] + ', ';
            }
            if (i == 'address_house_number') {
              strTmp += dict[i];
            }
          }
          card.adress = strTmp;
        }
        if (k == 'photo_names' && this.value[k] != null) {
          //дописать
        }
        if (k == 'garbage_classes' && this.value[k] != null) {
          card.class_trash=this.value[k];
        }
        if (k == 'request_date') {
          let tmp: string = this.value[k];
          let st = "";
          for (let i = 0; i < tmp.length; i++) {
            if (tmp[i] != 'T') {
              st += tmp[i];
            }
            else {
              break;
            }
          }
          card.request_date = st;
        }

        if (k == 'status') {
          if (this.value[k] == 'view') {
            card.status=this.value[k];
          }
          else{
            this.flag=false;
            break;
          }
        }
      }
      if(this.flag==true)
        {
          this.arrOptionReq[this.j++] = card;
        }
        else{
          this.flag=true;
        }
    }
    this.flag=true;
  }

  cleanReq()
  {
    this.j=0;
    this.mainCont=false;
    this.arrOptionReq=[];
    for (let key in this.res) {
      this.value = this.res[key];
      let card: Card = new Card();
      for (let k in this.value) {
        if (k == 'id') {
          card.id = this.value[k];
        }

        let strTmp = '';
        if (k == 'address') {
          let dict = this.value[k];
          for (let i in dict) {
            if (i == 'address_city') {
              strTmp += dict[i] + ', ';
            }
            if (i == 'address_street') {
              strTmp += dict[i] + ', ';
            }
            if (i == 'address_house_number') {
              strTmp += dict[i];
            }
          }
          card.adress = strTmp;
        }
        if (k == 'photo_names' && this.value[k] != null) {
          //дописать
        }
        if (k == 'garbage_classes' && this.value[k] != null) {
          card.class_trash=this.value[k];
        }
        if (k == 'request_date') {
          let tmp: string = this.value[k];
          let st = "";
          for (let i = 0; i < tmp.length; i++) {
            if (tmp[i] != 'T') {
              st += tmp[i];
            }
            else {
              break;
            }
          }
          card.request_date = st;
        }

        if (k == 'status') {
          if (this.value[k] == 'clean') {
            card.status=this.value[k];
          }
          else{
            this.flag=false;
            break;
          }
        }
      }
      if(this.flag==true)
        {
          this.arrOptionReq[this.j++] = card;
        }
        else{
          this.flag=true;
        }
    }
    this.flag=true;
  }
}