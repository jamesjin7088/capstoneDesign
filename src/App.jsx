import "./App.css";
import Header from "./components/Header";

import { Routes, Route } from "react-router-dom";
import Home from "./page/Home";
import Studio from "./page/Studio";
import Gallery from "./page/Gallery";
import Notfound from "./page/Notfound";

function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/studio" element={<Studio />}></Route>
        <Route path="/gallery" element={<Gallery />}></Route>
        <Route path="*" element={<Notfound />}></Route>
      </Routes>
    </div>
  );
}

export default App;
