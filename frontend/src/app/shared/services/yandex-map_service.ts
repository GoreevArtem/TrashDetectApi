import { Injectable } from '@angular/core';
import { GlobalConfig } from 'src/app/global';


declare var ymaps:any;

@Injectable()

export class YandexMapService {
  map: any;
  myPlacemark: any;
 
  initMap(lat:any, long: any) {
   
    ymaps.ready().done(() => this.createMap(lat, long));
  }
  
  private createMap(lat: any, long: any): void {
    this.map = new ymaps.Map('map', {
      center: [lat, long],
      zoom: 10,
      controls: ['zoomControl']
    });
      var sentAdress;
      if(GlobalConfig.flagMap==false)
      {
        sentAdress=GlobalConfig.adress;
      }
      else
      {
        sentAdress=localStorage.getItem('street');
      }
      
      var res=ymaps.geocode(sentAdress);
      var firstGeoObject = res.then(
          function(ress:any) {
          
          var coordinate=[];
          coordinate=ress.geoObjects.get(0).geometry.getCoordinates();
          localStorage.setItem('coor', String(coordinate));
          }
        );
      
      let input=localStorage.getItem('coor');
      let tmp=input?.split(',').map(Number);
      let mark = this.createPlacemark(tmp);
      this.map.geoObjects.add(mark);
      this.getAddress(mark,tmp);
  }

  // Создание метки.
  createPlacemark(coords: any) {
    return new ymaps.Placemark(coords, {
      iconCaption: 'поиск...'
    }, {
      preset: 'islands#violetDotIconWithCaption',
      draggable: true
    });
  }

// Определяем адрес по координатам (обратное геокодирование).
  getAddress(mark: any,coords: any) {
    mark.properties.set('iconCaption', 'поиск...');
    ymaps.geocode(coords).then((res: any) => {
      var firstGeoObject = res.geoObjects.get(0);
      mark.properties
        .set({
          // Формируем строку с данными об объекте.
          iconCaption: [
            // Название населенного пункта или вышестоящее административно-территориальное образование.
            firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
            // Получаем путь до топонима, если метод вернул null, запрашиваем наименование здания.
            firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
          ].filter(Boolean).join(', '),
          // В качестве контента балуна задаем строку с адресом объекта.
          balloonContent: firstGeoObject.getAddressLine()
        });
        GlobalConfig.adress=firstGeoObject.getAddressLine();
    });
  }
}