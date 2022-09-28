// JSX for displaying search results.

function SearchedBook(props) {
    let url = '/user/userbook' + props.isbn
    return (
      <div className="searched-book">
        <h3>{props.title}</h3>
        <p>{props.author}</p>
        <a href={url}> 
        <img src={props.image}/>
        </a>
        <p>--------------------------------------------------</p>
      </div>
    );
  }


function SearchedBookContainer() {
   const [searchedBooks, setSearchedBooks] = React.useState([]);
 
   React.useEffect(() => {
     fetch('/booksearchresults.json') 
     .then((response) => response.json())
     .then((data) => { 
        console.log(data)
      setSearchedBooks(data);})}, [])
    
  
   const bookResults = [];
 
   for (const currentBook of searchedBooks) {
     bookResults.push(
       <SearchedBook
         isbn={currentBook.isbn}
         title={currentBook.title}
         author={currentBook.author}
         image={currentBook.image}
       />
     );
   }
 
   return (
     <React.Fragment>
       <h2>Search Results</h2>
       <div>{bookResults}</div>
     </React.Fragment>
   );
 }
 
// ReactDOM.render(<SearchedBookContainer />, document.getElementById('root'));