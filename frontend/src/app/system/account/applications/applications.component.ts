import { Component, OnInit } from '@angular/core';
import { RequestUserService } from 'src/app/shared/services/requestUser.service';
import { Card } from 'src/app/shared/model/card.model';
import { Router } from '@angular/router';
import { GlobalConfig } from 'src/app/global';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.css']
})
export class ApplicationsComponent implements OnInit {
  mas = [{}];
  res: { [index: number]: any; } = {};
  count = 0;
  value: { [index: string]: any; } = {};
  arr: Card[] = [];
  j = 0;

  constructor(private reqUser: RequestUserService, private router:Router) { }
  ngOnInit(): void {
    this.reqUser.getRequests(100)
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
              card.photo_name=this.value[k];
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
              if(this.value[k]=='not view')
              {
                card.redFlag=true;
                card.yellowFlag=false;
                card.greenFlag=false;
                card.status = 'Не просмотрено';
              }
              if(this.value[k]=='view')
              {
                card.status = 'Просмотрено';
                card.redFlag=false;
                card.yellowFlag=true;
                card.greenFlag=false;
              }
              if(this.value[k]=='clean')
              {
                card.status = 'Мусор убран';
                card.redFlag=false;
                card.yellowFlag=false;
                card.greenFlag=true;
              }
            }
          }
          this.arr[this.j++] = card;
        }
      }
      );
  }
  mySubscription:any;
  update()
  {
    window.location.reload();
  }

  searchText = '';

  openCard(id:any){
    GlobalConfig.paramReq=id;
    localStorage.setItem('paramReq', id);
    this.router.navigate(['/system','account', 'card']);
  }
}

