import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { GlobalConfig } from 'src/app/global';
import { PhotoService } from 'src/app/shared/services/photo.service';
import { RequestUserService } from 'src/app/shared/services/requestUser.service';
import { YandexMapService } from '../../../shared/services/yandex-map_service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent {
  sentAdress=GlobalConfig.adress;
  file = GlobalConfig.path;
  image_src:any;
  base64data:any;
  isOpen = false;

  open() {
    this.isOpen = !this.isOpen;
  }

  isOpen2 = false;
  open2() {
    this.isOpen2 = !this.isOpen2;
  }

  constructor(private yandexMap: YandexMapService, private photoService:PhotoService,
    private reqUser:RequestUserService, private router:Router) { }
  ngOnInit(): void {
  this.yandexMap.initMap(56.323163, 43.866262);
  this.photoService.downloadPhoto(encodeURIComponent(""+this.file))
  .subscribe((blob:any)=>{
    this.image_src=window.URL.createObjectURL(blob);
  });
}
  sentReq()
  {
    const adress=GlobalConfig.adress;
    const photo_name=this.file;
    this.reqUser.createRequest({
      "address": adress,
      "photo_names": photo_name,
    }).subscribe((res)=>{
      this.router.navigate(['/system','account','applications']);
    })
  }
}

