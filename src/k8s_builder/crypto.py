"""
This file contains the crypto primatives required for this builder setup.
"""

__author__ = "gazzasaur"
__copyright__ = "gazzasaur"
__license__ = "MIT"


from typing import List, Tuple

import hashlib
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

"""
Using secp256r1 (aka prime256) as it is optimized for raspberry pis.
This may need to change some time soon.
"""
class Ca:
    """
    An example below.  The '1' in the common name is a generation number.
    Validity days is 75000.  Let's face it, you are going to foget to renew it,
    just set it to something long and monitor the age instead of swallowing the
    poison pill.

    x509.Name([
        x509.NameAttribute(x509.NameOID.DOMAIN_COMPONENT, 'example.com')
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'k8s'),
        x509.NameAttribute(x509.NameOID.ORGANIZATIONAL_UNIT_NAME, 'builder'),
        x509.NameAttribute(x509.NameOID.COMMON_NAME, 'Root CA 1')])
    """
    @staticmethod
    def generate_root_ca(certificate_subject: x509.Name, validity_days: int = 75000) -> Tuple[x509.Certificate, ec.EllipticCurvePrivateKey]:
        key = ec.generate_private_key(ec.SECP256R1)
        csr = x509.CertificateSigningRequestBuilder().subject_name(certificate_subject).sign(key, hashes.SHA256())

        cert = x509.CertificateBuilder().subject_name(
            x509.Name(certificate_subject)
        ).issuer_name(
            x509.Name(certificate_subject)
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(csr.public_key()), critical=False,
        ).sign(key, hashes.SHA256())

        return (cert, key)

    @staticmethod
    def generate_intermediate_ca(cluster_domain: str, root_certifate: x509.Certificate, root_key: ec.EllipticCurvePrivateKey) -> Tuple[x509.Certificate, ec.EllipticCurvePrivateKey]:
        certificate_name_suffix = [x for x in root_certifate.subject.rdns if not x.get_attributes_for_oid(x509.NameOID.COMMON_NAME)]
        certificate_subject = [x509.RelativeDistinguishedName([x509.NameAttribute(x509.NameOID.COMMON_NAME, cluster_domain)])] + certificate_name_suffix

        x509.RelativeDistinguishedName([x509.NameAttribute(x509.NameOID.COMMON_NAME, cluster_domain)])

        key = ec.generate_private_key(ec.SECP256R1)
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name(certificate_subject)).sign(key, hashes.SHA256())

        cert = x509.CertificateBuilder().subject_name(
            x509.Name(certificate_subject)
        ).issuer_name(
            root_certifate.subject
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            root_certifate.not_valid_after
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(root_certifate.public_key()), critical=False,
        ).sign(root_key, hashes.SHA256())

        return (cert, key)

    @staticmethod
    def generate_service_certifcate(namespace: str, service: str, domain: str, intermediate_certificate: x509.Certificate, intermediate_key: ec.EllipticCurvePrivateKey, validity_days: int = 3650):
        certificate_name_suffix = [x for x in intermediate_certificate.subject.rdns if not x.get_attributes_for_oid(x509.NameOID.COMMON_NAME)]
        certificate_subject = [x509.RelativeDistinguishedName([x509.NameAttribute(x509.NameOID.COMMON_NAME, '{}.{}.{}'.format(service, namespace, domain))])] + certificate_name_suffix

        key = ec.generate_private_key(ec.SECP256R1)
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name(certificate_subject)).sign(key, hashes.SHA256())

        validity = datetime.utcnow() + timedelta(days=validity_days);
        if validity > intermediate_certificate.not_valid_after:
            validity = intermediate_certificate.not_valid_after

        cert = x509.CertificateBuilder().subject_name(
            x509.Name(certificate_subject)
        ).issuer_name(
            intermediate_certificate.subject
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            validity
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        ).add_extension(
            x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False,
        ).add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(intermediate_certificate.public_key()), critical=False,
        ).sign(intermediate_key, hashes.SHA256())

        return (cert, key)
