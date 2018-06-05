class ClickButton extends React.Component {
	constructor(props) {
               super(props);
               this.state = {class: "off", label: "Нажми"};             
               this.press = this.press.bind(this);
           }
            press(e){
            	console.log(e);		
            	let className = (this.state.class==="off")?"on":"off";
            	this.setState({class: className});
           }
           render() {
               return <button onClick={this.press} className={this.state.class}>{this.state.label}</button>;
           }
}

function Docitem(props) {         
    return <li><div>
        <p>Регистрационный номер: {props.number}</p>
        <p>Статус: {props.status}</p>
    </div></li>;
}
Docitem.defaultProps = {number: "Where is my number", status: "Where is my status?"};

class Clock extends React.Component {
            constructor(props) {
              super(props);
              this.state = {date: new Date(), name: "Tom"};
            }
            componentDidMount() {
              this.timerId = setInterval(
                () => this.tick(),
                1000
              );
            }
           	componentWillUnmount() {
              clearInterval(this.timerId);
            }
       		tick() {
              this.setState({
                date: new Date()
              });
            }
            render() {
              return (
                <div>
                  <h1>Привет, {this.state.name}</h1>
                  <h2>Текущее время {this.state.date.toLocaleTimeString()}.</h2>
                </div>
              );
            }
          
}   

const propsValues = {
    title: "Список Деклараций",
    items: [
            {number : "00001", status:"upload"},
            {number : "00002", status:"upload"},
            {number : "00004", status:"upload"},
            {number : "00005", status:"loading"},
            {number : "00006"}
    ]
};

class Item extends React.Component {
            render() {
              return <li>{this.props.name}</li>;
            }
          }

class ItemsList extends React.Component {
	constructor(props){
        super(props);
        this.state = { items: this.props.data.items};
                 
        this.filterList = this.filterList.bind(this);
    }
    filterList(text){

        var filteredList = this.props.data.items.filter(function(item){
            return item.number.toLowerCase().search(text)!== -1;
        });
        // обновление состояния
        this.setState({items: filteredList});
    }

            render() {
              return(
              <div>         
                  <h2>{this.props.data.title}</h2>
                  <SearchPlugin filter={this.filterList} />
                  
                  <ul>
                	{
                    	this.state.items.map(function(item){
                    	    return <Docitem key={item} number={item.number} status={item.status} />
                    	})
            		}
                  </ul>
              </div>);
            }
          }

class SearchPlugin extends React.Component{
             
    constructor(props){
        super(props);
        this.onTextChanged = this.onTextChanged.bind(this);
    }
             
    onTextChanged(e){
        var text = e.target.value.trim();   // удаляем пробелы
        this.props.filter(text); // передаем введенный текст в родительский компонент
    }
             
    render() {
        return <input placeholder="Поиск" onChange={this.onTextChanged} />;
    }
}

ReactDOM.render(
    <div>
        <ItemsList data={propsValues} />
        <Clock/>	
        <ClickButton/>
    </div>,
    document.getElementById("container"),
    function(){ console.log("рендеринг элемента React");}
)