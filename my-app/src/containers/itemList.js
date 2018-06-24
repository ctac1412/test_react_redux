import { connect } from 'react-redux'
import { setItems } from '../actions'
import { getItems } from '../actions'
import itemList from '../components/itemList'

const mapStateToProps = state => ({
  items: state.items
})

const mapDispatchToProps = dispatch => ({
  onClickButton:(items)=>{
    // console.log(store)
    dispatch(setItems(items));
    // getItems();
    // fetchOnPress()
    // setItems(state)
  },
  onHoverButton:()=>{
    console.log("I'm hover");
  }
})
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(itemList)
