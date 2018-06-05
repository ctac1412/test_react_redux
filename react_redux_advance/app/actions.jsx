var addDocItem = function (DocItem) {
  return {
    type: "ADD_ITEM_DOC",
    DocItem
  }
};
var deleteDocItem = function (DocItem) {
  return {
    type: "DELETE_ITEM_DOC",
    DocItem
  }
};
 
module.exports = {addDocItem, deleteDocItem};