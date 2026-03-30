import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const login = (email) => {
        setUser({
            email,
            credits: 10,
            isPremium: false
        });
    };

    const logout = () => {
        setUser(null);
    };

    const useCredit = () => {
        if (user && user.credits > 0) {
            setUser({ ...user, credits: user.credits - 1 });
            return true;
        }
        return false;
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, useCredit }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
