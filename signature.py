from pyhanko import stamp
from pyhanko.pdf_utils import images
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields, signers, timestamps

# signer = signers.SimpleSigner.load_pkcs12(
#     pfx_file="certificate.p12", passphrase=b"123456"
# )
signer = signers.SimpleSigner.load(
    key_file="server.key", cert_file="server.crt", key_passphrase=b"123456"
)
timestamper = timestamps.HTTPTimeStamper(url="http://timestamp.digicert.com")


with open("document.pdf", "rb") as doc:
    writer = IncrementalPdfFileWriter(doc)
    with open("output1.pdf", "wb") as output:
        signers.sign_pdf(
            writer,
            signature_meta=signers.PdfSignatureMetadata(
                field_name="Signature", reason="Signed with PDF Sign"
            ),
            signer=signer,
            timestamper=timestamper,
            output=output,
        )


with open("document.pdf", "rb") as doc:
    writer = IncrementalPdfFileWriter(doc)

    fields.append_signature_field(
        writer,
        sig_field_spec=fields.SigFieldSpec(
            "Signature 1", on_page=1, box=(70, 550, 170, 600)
        ),
    )

    signature_metadata1 = signers.PdfSignatureMetadata(
        field_name="Signature 1", reason="Signed with PDF Sign on behalf of John Doe"
    )

    pdf_signer1 = signers.PdfSigner(
        signature_meta=signature_metadata1,
        signer=signer,
        timestamper=timestamper,
        stamp_style=stamp.StaticStampStyle(
            border_width=0,
            background=images.PdfImage("signature1.png"),
        ),
    )

    with open("output2.pdf", "wb") as output:
        pdf_signer1.sign_pdf(writer, output=output)


with open("output2.pdf", "rb") as doc:
    writer = IncrementalPdfFileWriter(doc)

    fields.append_signature_field(
        writer,
        sig_field_spec=fields.SigFieldSpec(
            "Signature 2", on_page=1, box=(220, 550, 320, 600)
        ),
    )

    signature_metadata2 = signers.PdfSignatureMetadata(
        field_name="Signature 2", reason="Signed with PDF Sign on behalf of Jack Bauer"
    )

    pdf_signer2 = signers.PdfSigner(
        signature_meta=signature_metadata2,
        signer=signer,
        timestamper=timestamper,
        stamp_style=stamp.StaticStampStyle(
            border_width=0,
            background=images.PdfImage("signature2.png"),
        ),
    )

    with open("output3.pdf", "wb") as output:
        pdf_signer2.sign_pdf(writer, output=output)
