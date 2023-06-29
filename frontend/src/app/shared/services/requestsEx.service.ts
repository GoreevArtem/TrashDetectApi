import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { GlobalConfig } from "src/app/global";
import { environment } from "src/app/environment";

@Injectable()
export class RequestsExService {
    constructor(private http: HttpClient){}
    private path1='expert/get_all_requests';
    private path2='expert/get_request';
    private path3='expert/set_view_status';

    getRequests(limit: number)
    {
        let params = `?limit=${limit}`;
        return this.http.get<any>(`${environment.api}${this.path1}`+params,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

    getRequest(id: number)
    {
        let params = `?req_id=${id}`;
        return this.http.get<any>(`${environment.api}${this.path2}`+params,{headers: new HttpHeaders({'Content-Type':'application/json','Authorization':'Bearer '+ GlobalConfig.t}) });
    }

    setViewStatus(id: number)
    {   
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${GlobalConfig.t}`})}; 
        return this.http.put(`${environment.api}${this.path3}?req_id=${id}`, id, httpOptions);
    }

}