export class Card {
    public id: number;
    public adress: string;
    public request_date: string;
    public status?: string;
    public redFlag?: boolean;
    public yellowFlag?: boolean;
    public greenFlag?: boolean;
    public notViewFlag?: boolean;
    public viewFlag?: boolean;
    public cleanFlag?: boolean;
    public photo_name?: any;
    public photo_src?: any;
    public class_trash?: string;
    constructor() {
        this.id=0;
        this.adress="";
        this.request_date="";
        this.status="";
     }
}