var Map = require("immutable").Map;
 
var reducer = function(state = Map(), action) {
  switch (action.type) {
    case "SET_STATE":
        return state.merge(action.state);
    case "ADD_ITEM_DOC":
        return state.update("docItems", () => docItems.push(action.DocItem));
    case "DELETE_ITEM_DOC":
        return state.update("docItems",
            (docItems) => docItems.filterNot(
                (DocItem) => DocItem === action.DocItem
            )
        );
  }
  return state;
}
module.exports = reducer;