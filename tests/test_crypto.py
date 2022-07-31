from time import sleep, time
import pytest

import time
from datetime import datetime, timedelta
from cryptography import x509
from k8s_builder import crypto
from cryptography.hazmat.primitives import hashes

__author__ = "gazzasaur"
__copyright__ = "gazzasaur"
__license__ = "MIT"


def test_generate_root_ca():
    root_certificate_subject = x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, 'Root CA 1'),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    (root_cert, root_key) = crypto.Ca.generate_root_ca(root_certificate_subject)

    assert root_cert.subject == root_certificate_subject
    assert root_cert.not_valid_before <= datetime.utcnow()
    assert root_cert.not_valid_after > datetime.utcnow() + timedelta(70000)


def test_generate_intermediate_ca():
    root_certificate_subject = x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, 'Root CA 1'),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    (root_cert, root_key) = crypto.Ca.generate_root_ca(root_certificate_subject)

    intermediate_name = 'Intermediate CA 1'
    (int_cert, int_key) = crypto.Ca.generate_intermediate_ca(intermediate_name, root_cert, root_key)

    assert int_cert.subject == x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, intermediate_name),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    assert int_cert.not_valid_before <= datetime.utcnow()
    assert int_cert.not_valid_after == root_cert.not_valid_after


def test_generate_intermediate_ca_not_before_based_on_now():
    root_certificate_subject = x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, 'Root CA 1'),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    (root_cert, root_key) = crypto.Ca.generate_root_ca(root_certificate_subject)

    time.sleep(1.0);

    intermediate_name = 'Intermediate CA 1'
    (int_cert, int_key) = crypto.Ca.generate_intermediate_ca(intermediate_name, root_cert, root_key)

    assert int_cert.subject == x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, intermediate_name),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    assert int_cert.not_valid_before <= datetime.utcnow()
    assert int_cert.not_valid_before > root_cert.not_valid_before
    assert int_cert.not_valid_after == root_cert.not_valid_after


def test_generate_intermediate_ca_no_root_common_name():
    root_certificate_subject = x509.Name([
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    (root_cert, root_key) = crypto.Ca.generate_root_ca(root_certificate_subject)

    intermediate_name = 'Intermediate CA 1'
    (int_cert, int_key) = crypto.Ca.generate_intermediate_ca(intermediate_name, root_cert, root_key)

    assert int_cert.subject == x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, intermediate_name),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    assert int_cert.not_valid_before <= datetime.utcnow()
    assert int_cert.not_valid_after == root_cert.not_valid_after


def test_generate_subject():
    root_certificate_subject = x509.Name([
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    (root_cert, root_key) = crypto.Ca.generate_root_ca(root_certificate_subject)

    (cert, key) = crypto.Ca.generate_service_certifcate("namespace", "service", "example.com", root_cert, root_key)

    assert cert.subject == x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, "service.namespace.example.com"),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    assert cert.not_valid_before <= datetime.utcnow()
    assert cert.not_valid_after <= root_cert.not_valid_after


def test_generate_subject_bound_validity():
    root_certificate_subject = x509.Name([
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    (root_cert, root_key) = crypto.Ca.generate_root_ca(root_certificate_subject)

    root_cert = x509.CertificateBuilder().subject_name(
            x509.Name(root_cert.subject)
        ).issuer_name(
            x509.Name(root_cert.subject)
        ).public_key(
            root_cert.public_key()
        ).serial_number(
            root_cert.serial_number
        ).not_valid_before(
            root_cert.not_valid_before
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=1)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(root_cert.public_key()), critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(root_cert.public_key()), critical=False,
        ).sign(root_key, hashes.SHA256())

    (cert, key) = crypto.Ca.generate_service_certifcate("namespace", "service", "example.com", root_cert, root_key)

    assert cert.subject == x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, "service.namespace.example.com"),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')])
    assert cert.not_valid_before <= datetime.utcnow()
    assert cert.not_valid_after == root_cert.not_valid_after
