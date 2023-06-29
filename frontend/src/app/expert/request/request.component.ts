import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RequestsExService } from 'src/app/shared/services/requestsEx.service';
import { YandexMapService } from 'src/app/shared/services/yandex-map_service';
import { Card } from 'src/app/shared/model/card.model';
import { GlobalConfig } from 'src/app/global';

@Component({
  selector: 'app-request',
  templateUrl: './request.component.html',
  styleUrls: ['./request.component.css']
})
export class RequestComponent {
  sentAdress=localStorage.getItem('street');
  isOpen = false;
  dict: { [index: string]: any; } = {};
  card: Card = new Card();
  arr: Card[] = [];
  notViewFlag = false;
  viewFlag = false;

  constructor(private yandexMap: YandexMapService, private router:Router, private reqEx:RequestsExService) { }
  ngOnInit(): void {
  this.yandexMap.initMap(56.323163, 43.866262);
  this.reqEx.getRequest(GlobalConfig.paramReq)
  .subscribe(res => {
    this.dict = res;
    for (let k in this.dict) {
      if (k == 'id') {
        this.card.id = this.dict[k];
      }

      let strTmp = '';
      if (k == 'address') {
        let dict = this.dict[k];
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
        this.card.adress = strTmp;
        GlobalConfig.adress=this.card.adress;
      }
      if (k == 'photo_names' && this.dict[k] != null) {
        //дописать
      }
      if (k == 'request_date') {
        let tmp: string = this.dict[k];
        let st = "";
        for (let i = 0; i < tmp.length; i++) {
          if (tmp[i] != 'T') {
            st += tmp[i];
          }
          else {
            break;
          }
        }
        this.card.request_date = st;
      }

      if (k == 'status') {

        if (this.dict[k] == 'not view') {
          this.card.status = 'Просмотрено';
          this.notViewFlag = true;
        }
        if (this.dict[k] == 'view') {
          this.card.status = 'Мусор убран';
          this.viewFlag = true;
        }
      }
    }
    this.arr.push(this.card);
  });
  }

  open() {
    this.isOpen = !this.isOpen;
  }

  view(id:any)
  {
    this.reqEx.setViewStatus(id)
    .subscribe(res=>{
      console.log(res);
    })
  }
}
