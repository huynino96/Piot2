import { useState, useContext } from 'react';
import { useRouter } from 'next/router';
import AppContext from '../../context/AppContext';
import {
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,
} from "reactstrap";
import Link from 'next/link'
import {isRole} from "../../utils/helpers";

const Header = () => {
    const [isOpen, setIsOpen] = useState(false);
    const { authenticated, setAuthenticated } = useContext(AppContext);
    const router = useRouter();
    const toggle = () => setIsOpen(!isOpen);

    const handleLogout = () => {
        window.localStorage.removeItem('access_token');
        setAuthenticated(false);
        router.push('/');
    };

    return (
        <Navbar color="dark" dark expand="md">
            <Link href="/">
                <NavbarBrand>Auto Salon</NavbarBrand>
            </Link>
            <NavbarToggler onClick={toggle}/>
            <Collapse isOpen={isOpen} navbar>
                <Nav className="mr-auto" navbar>
                    {isRole('admin') && (
                        <>
                            <NavItem>
                                <Link href="/admin">
                                    <NavLink>Cars</NavLink>
                                </Link>
                            </NavItem>
                            <NavItem>
                                <Link href="/admin/users">
                                    <NavLink>Users</NavLink>
                                </Link>
                            </NavItem>
                            <NavItem>
                                <Link href="/admin/histories">
                                    <NavLink>Car Rental History</NavLink>
                                </Link>
                            </NavItem>
                            <NavItem>
                                <Link href="/admin/reports">
                                    <NavLink>Reports</NavLink>
                                </Link>
                            </NavItem>
                        </>
                    )}
                    {isRole('maanger') && (
                        <NavItem>
                            <Link href="/manager">
                                <NavLink>Manager</NavLink>
                            </Link>
                        </NavItem>
                    )}
                    {isRole('user') && (
                        <>
                            <NavItem>
                                <Link href="/user">
                                    <NavLink>Available Car</NavLink>
                                </Link>
                            </NavItem>
                            <NavItem>
                                <Link href="/user/histories">
                                    <NavLink>Booked Car</NavLink>
                                </Link>
                            </NavItem>
                            <NavItem>
                                <Link href="/user/issue">
                                    <NavLink>Report an issue</NavLink>
                                </Link>
                            </NavItem>
                        </>
                    )}
                    {!authenticated && (
                        <>
                            <NavItem>
                                <Link href="/auth/login">
                                    <NavLink>Login</NavLink>
                                </Link>
                            </NavItem>
                            <NavItem>
                                <Link href="/auth/register">
                                    <NavLink>Register</NavLink>
                                </Link>
                            </NavItem>
                        </>
                    )}
                </Nav>
                {authenticated && (
                    <Nav className="ml-auto" navbar>
                        <NavItem>
                            <NavLink onClick={handleLogout}>Logout</NavLink>
                        </NavItem>
                    </Nav>
                )}
            </Collapse>
        </Navbar>
    );
};

export default Header;
