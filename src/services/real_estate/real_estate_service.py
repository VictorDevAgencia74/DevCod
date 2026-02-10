from src.database import db
from src.models.real_estate.models import Imovel, ImagemImovel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

class RealEstateService:
    @staticmethod
    def init_defaults():
        # Se não houver imóveis, cria tudo do zero
        if Imovel.query.count() == 0:
            # Imóvel 1
            imovel1 = Imovel(
                titulo="Apartamento de Luxo no Centro",
                descricao="Lindo apartamento com vista panorâmica, acabamento em mármore e área de lazer completa. O condomínio oferece piscina aquecida, academia de última geração e salão de festas.",
                preco=850000.00,
                tipo="Apartamento",
                area=120.0,
                quartos=3,
                banheiros=2,
                vagas=2,
                endereco="Av. Paulista, 1000 - Centro",
                imagem_url="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            )
            db.session.add(imovel1)
            db.session.commit()
            
            RealEstateService._add_images(imovel1, [
                ("https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Sala de Estar"),
                ("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Quarto Principal"),
                ("https://images.unsplash.com/photo-1556911220-e15b29be8c8f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Cozinha Gourmet"),
                ("https://images.unsplash.com/photo-1584622050111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Banheiro")
            ])

            # Imóvel 2
            imovel2 = Imovel(
                titulo="Casa Moderna em Condomínio",
                descricao="Casa térrea com piscina, churrasqueira e segurança 24h. Projeto arquitetônico premiado, com ampla iluminação natural e integração entre ambientes.",
                preco=1200000.00,
                tipo="Casa",
                area=250.0,
                quartos=4,
                banheiros=4,
                vagas=4,
                endereco="Rua das Palmeiras, 500 - Jardim Verde",
                imagem_url="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            )
            db.session.add(imovel2)
            db.session.commit()

            RealEstateService._add_images(imovel2, [
                ("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Fachada"),
                ("https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Área Externa com Piscina"),
                ("https://images.unsplash.com/photo-1484154218962-a1c002085d2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Sala de Jantar"),
                ("https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Suíte Master")
            ])

            # Imóvel 3
            imovel3 = Imovel(
                titulo="Studio Compacto e Funcional",
                descricao="Ideal para investidores ou solteiros. Próximo ao metrô. Totalmente mobiliado com móveis planejados de alta qualidade.",
                preco=350000.00,
                tipo="Studio",
                area=35.0,
                quartos=1,
                banheiros=1,
                vagas=0,
                endereco="Rua Augusta, 200 - Centro",
                imagem_url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
            )
            db.session.add(imovel3)
            db.session.commit()

            RealEstateService._add_images(imovel3, [
                ("https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Visão Geral"),
                ("https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Home Office"),
                ("https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Cozinha Americana")
            ])
        
        # Se os imóveis já existem mas as imagens não (caso de update), popula as imagens
        elif ImagemImovel.query.count() == 0:
            imoveis = Imovel.query.all()
            for imovel in imoveis:
                if imovel.tipo == "Apartamento":
                    RealEstateService._add_images(imovel, [
                        (imovel.imagem_url, "Sala de Estar"),
                        ("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Quarto Principal"),
                        ("https://images.unsplash.com/photo-1556911220-e15b29be8c8f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Cozinha Gourmet"),
                        ("https://images.unsplash.com/photo-1584622050111-993a426fbf0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Banheiro")
                    ])
                elif imovel.tipo == "Casa":
                    RealEstateService._add_images(imovel, [
                        (imovel.imagem_url, "Fachada"),
                        ("https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Área Externa com Piscina"),
                        ("https://images.unsplash.com/photo-1484154218962-a1c002085d2f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Sala de Jantar"),
                        ("https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Suíte Master")
                    ])
                elif imovel.tipo == "Studio":
                    RealEstateService._add_images(imovel, [
                        (imovel.imagem_url, "Visão Geral"),
                        ("https://images.unsplash.com/photo-1554995207-c18c203602cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Home Office"),
                        ("https://images.unsplash.com/photo-1493809842364-78817add7ffb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", "Cozinha Americana")
                    ])

    @staticmethod
    def _add_images(imovel, images_data):
        for url, desc in images_data:
            img = ImagemImovel(imovel_id=imovel.id, url=url, descricao=desc)
            db.session.add(img)
        db.session.commit()

    @staticmethod
    def listar_imoveis():
        return Imovel.query.all()

    @staticmethod
    def get_imovel(id):
        return Imovel.query.get(id)

    @staticmethod
    def gerar_pdf_proposta(imovel_id, cliente_nome, cliente_email, valor_proposta):
        imovel = Imovel.query.get(imovel_id)
        if not imovel:
            return None

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Cabeçalho
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height - 50, "Fuosteck Real Estate")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, "Soluções Digitais para o Mercado Imobiliário")
        
        c.line(50, height - 80, width - 50, height - 80)

        # Título do Documento
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 120, "PROPOSTA DE INTENÇÃO DE COMPRA")

        # Dados do Imóvel
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 160, "Detalhes do Imóvel:")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 180, f"Imóvel: {imovel.titulo}")
        c.drawString(50, height - 200, f"Endereço: {imovel.endereco}")
        c.drawString(50, height - 220, f"Valor Anunciado: R$ {imovel.preco:,.2f}")
        c.drawString(50, height - 240, f"Área: {imovel.area} m² | Quartos: {imovel.quartos} | Vagas: {imovel.vagas}")

        # Dados do Cliente
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 280, "Dados do Proponente:")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 300, f"Nome: {cliente_nome}")
        c.drawString(50, height - 320, f"Email: {cliente_email}")

        # A Proposta
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 360, "Condições da Proposta:")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 390, f"Valor Oferecido: R$ {float(valor_proposta):,.2f}")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 420, "Esta proposta tem validade de 7 dias úteis e está sujeita à aprovação do proprietário.")
        c.drawString(50, height - 435, "Este documento não possui valor de escritura pública, servindo apenas como formalização de interesse.")

        # Rodapé
        c.line(50, 100, width - 50, 100)
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width / 2, 80, "Gerado automaticamente pelo Sistema Fuosteck Real Estate")
        c.drawCentredString(width / 2, 65, "www.fuosteck.com.br")

        c.showPage()
        c.save()
        
        buffer.seek(0)
        return buffer
