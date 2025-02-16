import "./App.css"
import SearchBar from "./components/SearchBar"
import Masonry from "./components/Masonry"
import QueryCard from "./components/QueryCrad"
import Loader from "./components/Loader"

const App = () => {
  return (
    <div className="App">
    <div className="min-h-screen p-4">
      <SearchBar />
      <Masonry />
      <Loader />
      <QueryCard />
    </div>
    </div>
  )
}

export default App
