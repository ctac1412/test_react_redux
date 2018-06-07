import { connect } from 'react-redux'
import { setItems } from '../actions'
import itemList from '../components/itemList'
const defData = [
  'item1',
  'item2',
  'item3',
  'item4',
]
const mapStateToProps = state => ({
  items: state.items
})
const mapDispatchToProps = dispatch => ({
  onClickButton:()=>{
    console.log("I've clicked");
    dispatch(setItems(defData));
  },
  onHoverButton:()=>{
    console.log("I'm hover");
  }
})
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(itemList)
