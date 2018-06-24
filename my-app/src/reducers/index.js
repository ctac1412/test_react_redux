import { ADD_ARTICLE } from "../constants/action-types";
const initialState = {
  items:[],
  articles: [],
  isLoading:false
}

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case ADD_ARTICLE:
      return { ...state, articles: [...state.articles, action.payload] };
    default:
      return state;
  }
};
// {
//   switch (action.type) {
//     case 'SET_ITEMS':
//       return {
//           ...state,
//           items:action.items,
//           isLoading:false
//       }
//     case 'GET_ITEMS':
//     return {
//         ...state,
//         items:action.items,
//         isLoading:false
//     } 
//     default:
//       return state
//   };
// }
export default reducer
