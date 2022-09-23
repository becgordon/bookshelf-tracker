// JSX for React components.

function UserBook(props) {
    return (
      <div className="user-book">
        <h3>{props.title}</h3>
        <p>{props.author}</p>
        <img src={props.image}/>
      </div>
    );
  }


function UserBookContainer() {
   const [userBooks, setUserBooks] = React.useState([]);
 
   React.useEffect(() =>{
     fetch('/userprofile/{user.username}')
     .then((response) => response.json())
     .then((data) => setUserBooks(data.userBooks))
   }, [])
   
 
   const books = [];
 
   for (const book of userBooks) {
     books.push(
       <UserBook
         isbn={book.isbn}
         title={book.title}
         author={book.author}
         image={book.image}
       />
     );
   }
 
   // returning the cards inside a div in the HTML
   return (
     <React.Fragment>
       <h2>My Library</h2>
       <div>{userBooks}</div>
     </React.Fragment>
   );
 }
 
 ReactDOM.render(<UserBookContainer />, document.getElementById('root'));