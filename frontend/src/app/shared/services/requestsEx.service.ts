import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { environment } from "src/app/environment";
import { JWT_NAME } from "./auth.service";

@Injectable()
export class RequestsExService {
    constructor(private http: HttpClient){}
    private path1='expert/get_all_requests';
    private path2='expert/get_request';
    private path3='expert/set_view_status';
    private path4='expert/set_clean_status';

    getRequests(limit: number)
    {
        let params = `?limit=${limit}`;
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.get<any>(`${environment.api}${this.path1}`+params,httpOptions);
    }

    getRequest(id: number)
    {
        let params = `?req_id=${id}`;
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.get<any>(`${environment.api}${this.path2}`+params,httpOptions);
    }

    setViewStatus(id: number)
    {   
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.put(`${environment.api}${this.path3}?req_id=${id}`, id, httpOptions);
    }

    setCleanStatus(id: number)
    {   
        const httpOptions = {headers: new HttpHeaders({'Content-Type':'application/json','Authorization':`Bearer ${localStorage.getItem(JWT_NAME)}`})}; 
        return this.http.put(`${environment.api}${this.path4}?req_id=${id}`, id, httpOptions);
    }
}