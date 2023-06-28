import { Component } from '@angular/core';
import { RequestUserService } from 'src/app/shared/services/requestUser.service';
import { YandexMapService } from '../../../shared/services/yandex-map_service';
import { GlobalConfig } from 'src/app/global';
import { Card } from 'src/app/shared/model/card.model';
import { PhotoService } from 'src/app/shared/services/photo.service';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent {
  sentAdress = localStorage.getItem('street');
  isOpen = false;
  dict: { [index: string]: any; } = {};
  card: Card = new Card();
  arr: Card[] = [];
  blockTrash=false;
  image_src:any;
  base64data:any;

  constructor(private yandexMap: YandexMapService, private reqUser: RequestUserService,
    private photoService:PhotoService) { }
  ngOnInit(): void {
    
    this.reqUser.getRequest(GlobalConfig.paramReq)
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
            this.photoService.downloadPhoto(encodeURIComponent(""+this.dict[k]))
            .subscribe((blob:any)=>{
              this.card.photo_src=window.URL.createObjectURL(blob);
            });
          }
          if (k == 'garbage_classes' && this.dict[k] != null) {
            this.card.class_trash=this.dict[k];
            this.blockTrash=true;
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
            if(this.dict[k]=='not view')
            {
              this.card.redFlag=true;
              this.card.yellowFlag=false;
              this.card.greenFlag=false;
              this.card.status = 'Не просмотрено';
            }
            if(this.dict[k]=='view')
            {
              this.card.status = 'Просмотрено';
              this.card.redFlag=false;
              this.card.yellowFlag=true;
              this.card.greenFlag=false;
            }
            if(this.dict[k]=='clean')
            {
              this.card.status = 'Мусор убран';
              this.card.redFlag=false;
              this.card.yellowFlag=false;
              this.card.greenFlag=true;
            }
          }
        }
        this.arr.push(this.card);
      });
      this.yandexMap.initMap(56.323163, 43.866262);
  }

  open() {
    this.isOpen = !this.isOpen;
  }
}
