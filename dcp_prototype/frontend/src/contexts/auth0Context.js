import { navigate } from "gatsby"
import React, { useContext, useEffect, useState } from "react"
import createAuth0Client from "@auth0/auth0-spa-js"

const config = {
  domain: process.env.AUTH0_DOMAIN,
  client_id: process.env.AUTH0_CLIENTID,
  redirect_uri: "http://localhost:8000",
}

export const Auth0Context = React.createContext()
export const useAuth0 = () => useContext(Auth0Context)
const Auth0Provider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [auth0Client, setAuth0] = useState()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth0 = async () => {
      const auth0FromHook = await createAuth0Client(config)
      setAuth0(auth0FromHook)
      console.log("auth0FromHook", auth0FromHook)
      if (
        window.location.search.includes("code=") &&
        window.location.search.includes("state=")
      ) {
        const { appState } = await auth0FromHook.handleRedirectCallback()
        let requestPath = window.localStorage.getItem("requestPath")
        console.log("redirect requestPath", requestPath)
        if (requestPath) {
          window.localStorage.removeItem("requestPath")
          navigate(requestPath)
        }
      }

      const isAuthenticated = await auth0FromHook.isAuthenticated()
      console.log("isAuthenticated", isAuthenticated)
      setIsAuthenticated(isAuthenticated)

      if (isAuthenticated) {
        const user = await auth0FromHook.getUser()
        console.log("user", user)
        setUser(user)
      }

      setLoading(false)
    }

    initAuth0()
    // eslint-disable-next-line
  }, [])

  const loginWithRedirect = async (...p) => {
    if (window.localStorage.getItem("requestPath") === null) {
      window.localStorage.setItem("requestPath", window.location.pathname + window.location.search)
    }
    await auth0Client.loginWithRedirect(...p)
  }

  const handleRedirectCallback = async () => {
    setLoading(true)
    await auth0Client.handleRedirectCallback()
    const user = await auth0Client.getUser()
    setLoading(false)
    setIsAuthenticated(true)
    setUser(user)

    // Return to original page
    let requestPath = window.localStorage.getItem("requestPath")
    console.log("requestPath", requestPath)
    if (requestPath) {
      window.localStorage.removeItem("requestPath")
      navigate(requestPath)
    }
  }

  return (
    <Auth0Context.Provider
      value={{
        isAuthenticated,
        user,
        loading,
        handleRedirectCallback,
        loginWithRedirect,
        getIdTokenClaims: (...p) => auth0Client.getIdTokenClaims(...p),
        getTokenSilently: (...p) => auth0Client.getTokenSilently(...p),
        logout: (...p) => auth0Client.logout(...p),
      }}
    >
      {children}
    </Auth0Context.Provider>
  )
}

export default Auth0Context

export { Auth0Provider }