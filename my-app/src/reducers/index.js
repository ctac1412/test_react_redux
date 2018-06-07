const reducer = (state = {
  items:[],
  isLoading:false
}, action) => {
  switch (action.type) {
    case 'SET_ITEMS':
      return {
          ...state,
          items:action.items,
          isLoading:false
      }
    default:
      return state
  };
}
export default reducer
