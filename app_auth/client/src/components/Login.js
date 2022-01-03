import "./Login.css";
import { Form, Button, Card } from "react-bootstrap";
import { Link, useHistory } from "react-router-dom";
import { useState } from "react";

function Login({ onSuccess }) {
  let history = useHistory();
  // hook to add a state to a component
  const [error, setError] = useState(false);

  async function handleSubmit(e) {
    // Isto irá bloquear o comportamento nativo do form (fazer um POST request com os dados de login)
    e.preventDefault();

    if (error) return;

  }

  const queryString = window.location.search;
  console.log(queryString);

  const urlParams = new URLSearchParams(queryString);
  if(urlParams.has('username')){
    const store = {
      username: urlParams.get('username'),
      role: urlParams.get('role'),
    };
    localStorage.setItem("user", JSON.stringify(store));
    history.push("/characters");
  }

  return (
    <Card
      style={{
        width: "18rem",
        opacity: 1,
        borderRadius: 20,
        backgroundColor: "#d39e00",
        marginTop: "5rem",
        padding: "1rem",
        maxHeight: 500,
      }}
    >
      <Card.Body>
        <Form onSubmit={handleSubmit}>
          <h1 className="form-title">Login</h1>
          <p></p>
          <p></p>
          <div className="form-controls">
            <Button
              style={{ width: "5rem", marginLeft: "35%" }}
              variant="dark"
              type="submit"
              href="https://localhost:8443"
            >
              Login
            </Button>
            <p></p>
            <Link className="continue-link" to="/characters">
              Continuar sem login
            </Link>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
}

export default Login;
