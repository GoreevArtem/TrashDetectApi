import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RequestsExService } from 'src/app/shared/services/requestsEx.service';
import { YandexMapService } from 'src/app/shared/services/yandex-map_service';
import { Card } from 'src/app/shared/model/card.model';
import { GlobalConfig } from 'src/app/global';
import { PhotoService } from 'src/app/shared/services/photo.service';

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
  id:number=0;
  tmp:any;
  constructor(private yandexMap: YandexMapService, private router:Router,
    private reqEx:RequestsExService, private photoService:PhotoService) { }
  ngOnInit(): void {
  this.yandexMap.initMap(56.323163, 43.866262);
  let store = localStorage.getItem('idReq')
  let obj = store !== null ? JSON.parse(store) : null;
  this.id=obj.idReq;
  this.reqEx.getRequest(this.id)
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
        this.photoService.downloadPhotoEx(this.id)
        .subscribe((blob:any)=>{
          this.card.photo_src=window.URL.createObjectURL(blob);
        });
      }
      if (k == 'garbage_classes' && this.dict[k] != null) {
        this.card.class_trash=this.dict[k];
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
          this.card.notViewFlag = true;
          this.card.viewFlag = false;
          this.card.cleanFlag=false;
        }
        if (this.dict[k] == 'view') {
          this.card.status = 'Мусор убран';
          this.card.notViewFlag = false;
          this.card.viewFlag = true;
          this.card.cleanFlag=false;
        }
        if (this.dict[k] == 'clean') {
          this.card.status = 'Мусор больше нет по этому адресу';
          this.card.notViewFlag = false;
          this.card.viewFlag = false;
          this.card.cleanFlag=true;
        }
      }
    }
    this.arr.push(this.card);
    console.log('ARRR=',this.arr);
  });
  
  }

  open() {
    this.isOpen = !this.isOpen;
  }

  view(id:any)
  {
    this.reqEx.setViewStatus(id)
    .subscribe(res=>{
     this.router.navigate(['expert','requests']);
    })
  }
  clean(id:any)
  {
    this.reqEx.setCleanStatus(id)
    .subscribe(res=>{
     this.router.navigate(['expert','requests']);
    })
  }

  noTrash()
  {
    this.router.navigate(['expert','requests']);
  }

}
