import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { GlobalConfig } from "src/app/global";
import { environment } from "src/app/environment";

@Injectable()
export class RequestUserService {
    constructor(private http: HttpClient){}
    private path1='request/create_request';
    private path2='request/get_requests';
    private path3='request/get_request';

    createRequest(data:any)
    {
        return this.http.post<any>(`${environment.api}${this.path1}`,data,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

    getRequests(limit: number)
    {
        let params = `?limit=${limit}`;
        return this.http.get<any>(`${environment.api}${this.path2}`+params,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

    getRequest(id: number)
    {
        let params = `?req_id=${id}`;
        return this.http.get<any>(`${environment.api}${this.path3}`+params,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

 
}