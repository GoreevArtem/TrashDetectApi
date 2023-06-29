import { Component, OnInit } from '@angular/core';
import { ExpertService } from 'src/app/shared/services/expert.service';
import { GlobalConfig } from 'src/app/global';
import { Router } from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { matchpassword } from 'src/app/auth/matchpassword.validator';
import { Card } from 'src/app/shared/model/card.model';
import { RequestsExService } from 'src/app/shared/services/requestsEx.service';

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
  j = 0;

  constructor(private expertService:ExpertService, private router:Router, private reqEx:RequestsExService) { }
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

    this.reqEx.getRequests(2)
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
    GlobalConfig.paramReq=id;
    this.router.navigate(['/expert','request']);
  }

  logout()
  {
    GlobalConfig.t="";
    this.router.navigate(['/system', 'about-us']);
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
    this.mainCont=false;
  }

  close1()
  {
    this.isOpen1=false;
    this.form1.reset();
  }
}