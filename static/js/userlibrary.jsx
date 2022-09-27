// JSX for displaying user's library.

function UserBook(props) {
    let url = '/user/userbook' + props.isbn
    return (
      <div className="user-book">
        <h3>{props.title}</h3>
        <p>{props.author}</p>
        <a href={url}> 
        <img src={props.image}/>
        </a>
        <p>--------------------------------------------------</p>
      </div>
    );
  }
// needs image to go to correct page, not rendering correctly

function UserBookContainer() {
   const [userBooks, setUserBooks] = React.useState([]);
 
   React.useEffect(() => {
     fetch('/userbooks.json') 
     .then((response) => response.json())
     .then((data) => { 
      setUserBooks(data);})}, [])
    
  
   const books = [];
 
   for (const currentBook of userBooks) {
     books.push(
       <UserBook
         isbn={currentBook.isbn}
         title={currentBook.title}
         author={currentBook.author}
         image={currentBook.image}
       />
     );
   }
 
   return (
     <React.Fragment>
       <h2>My Library</h2>
       <div>{books}</div>
     </React.Fragment>
   );
 }
 
ReactDOM.render(<UserBookContainer />, document.getElementById('root'));
// ReactDOM.render(<h1>I'm a react render</h1>, document.getElementById('root'));