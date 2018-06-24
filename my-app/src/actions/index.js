import { ADD_ARTICLE } from "../constants/action-types";
export const addArticle = article => ({ type: ADD_ARTICLE, payload: article });


export const setItems = function(items) {
  console.log(items)  
  return {
  type:'SET_ITEMS',
  items
}};

export const getItems = function(){
  let items=[]
    return fetch("https://api.github.com").then(response=>{

    var s = new Date().getSeconds();
    for (let index = 0; index < s; index++) {
      
      items.push({"numbers":s,"state":"load"})
    }
    console.log(items)
  }).then(()=>{
  return {
    type:'GET_ITEMS',
    items
  }})
}

// =()=>(dispatch,getStore)=>{
//   dispatch(iveStartedTheFetch());
//   fetch(url).then().then(json=>{
//   dispatch(iveReceivedSomeData(json))
//   }).catch(e=>dispatch(ohFuck(e)))
//   }