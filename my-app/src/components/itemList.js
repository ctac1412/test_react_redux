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
          this.props.items.map(function(item){
            var a = new Date()
              return (<li>{item} {a}</li>)
          })
    }
      </ul>
      <button onClick={this.props.onClickButton}>SET ITEMS</button>
      </div>
    );
  }
}

export default ItemList;
