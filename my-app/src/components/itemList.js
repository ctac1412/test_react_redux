import React, { Component } from 'react';

class ItemList extends Component {
  constructor(props) {
      super(props);
      console.log(props);
  }
  
  render() {
    return (

      <div>
      <ul>
      {
          this.props.items.map(function(item, index){
              return (<li key={index}>{item.number}</li>)
          })
    }
      </ul>
      <button onClick={this.props.onClickButton}>GET ITEMS</button>
      </div>
    );
  }
}

export default ItemList;
