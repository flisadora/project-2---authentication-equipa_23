import "./App.css";
import Login from "./components/Login";
import Wiki from "./components/Wiki";
import Characters from "./components/Characters";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  BrowserRouter as Router,
  Route,
  Switch,
  NavLink,
} from "react-router-dom";
import { Container, Navbar, Nav } from "react-bootstrap";
import { useState, useEffect } from "react";

function App() {
  const [username, setUsername] = useState();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));

    if (user) {
      setUsername(user.username);
    }
  }, []);

  function handleClickLogout() {
    setUsername();
    localStorage.removeItem("user");
  }

  function handleSuccess(username) {
    setUsername(username);
  }

  return (
    <Router>
      <Navbar>
        <Container>
          <Navbar.Brand href="#home">
            <img
              src="https://vignette3.wikia.nocookie.net/logopedia/images/9/9c/HarryPotter.png/revision/latest?cb=20160624203951"
              height="80"
              className="d-inline-block align-top"
              alt="Harry Potter logo"
              width="250"
            />
          </Navbar.Brand >
          {username && <Nav style={{color: "#666", textDecoration: "none", textTransform: "uppercase", letterSpacing: "1px" }} >{username}</Nav>}
          {username ? (
            <Nav   style={{backgroundColor: "#333", padding: "10px", borderRadius: "20px", color: "#fff"}}>
              <NavLink style={{color: "#fff", textDecoration: "none", textTransform: "uppercase", letterSpacing: "1px" }} to="/" onClick={handleClickLogout}>
                Logout
              </NavLink>
            </Nav>
          ) : (
            <Nav style={{backgroundColor: "#333", padding: "10px", borderRadius: "20px", color: "#fff"}} >
              <NavLink style={{color: "#fff", textDecoration: "none", textTransform: "uppercase", letterSpacing: "1px" }} to="/">Login</NavLink>
            </Nav>
          )}
        </Container>
      </Navbar>
      <Switch>
        <Route path="/wiki">
          <div className="main">
            <Wiki />
          </div>
        </Route>
        <Route path="/characters">
          <div className="main">
            <Characters />
          </div>
        </Route>
        <Route path="/">
          <div className="main">
            <Login onSuccess={handleSuccess} />
          </div>
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
