import {useState} from "react";
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

const Header = () => {
    const [isOpen, setIsOpen] = useState(false);
    const toggle = () => setIsOpen(!isOpen);
    return (
        <Navbar color="dark" dark expand="md">
            <Link href="/">
                <NavbarBrand>Auto Salon</NavbarBrand>
            </Link>
            <NavbarToggler onClick={toggle}/>
            <Collapse isOpen={isOpen} navbar>
                <Nav className="mr-auto" navbar>
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
                    <NavItem>
                        <Link href="/manager">
                            <NavLink>Manager</NavLink>
                        </Link>
                    </NavItem>
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
                </Nav>
                <Nav className="ml-auto" navbar>
                    <NavItem>
                        <NavLink href="/">Logout</NavLink>
                    </NavItem>
                </Nav>
            </Collapse>
        </Navbar>
    );
};

export default Header;
